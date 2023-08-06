# This is adapted from stanza
import sys
from .seq2seq_model import Seq2SeqModel
from ..utils.seq2seq_utils import *
from ..utils.seq2seq_vocabs import *
from ..iterators.lemmatizer_iterators import LemmaDataLoader
from ..utils.base_utils import *


def set_lemma(doc, preds, obmit_tag):
    wid = 0
    for sentence in doc:
        for token in sentence[TOKENS]:
            if type(token[ID]) == int or len(token[ID]) == 1:
                token[LEMMA] = preds[wid]
                wid += 1

                if obmit_tag:
                    if UPOS in token:
                        del token[UPOS]
                    if XPOS in token:
                        del token[XPOS]
                    if FEATS in token:
                        del token[FEATS]
                    if HEAD in token:
                        del token[HEAD]
                    if DEPREL in token:
                        del token[DEPREL]
            else:
                for word in token[EXPANDED]:
                    word[LEMMA] = preds[wid]
                    wid += 1

                    if obmit_tag:
                        if UPOS in word:
                            del word[UPOS]
                        if XPOS in word:
                            del word[XPOS]
                        if FEATS in token:
                            del token[FEATS]
                        if HEAD in word:
                            del word[HEAD]
                        if DEPREL in word:
                            del word[DEPREL]
    return doc


class Trainer(object):
    """ A trainer for training models. """

    def __init__(self, args=None, vocab=None, emb_matrix=None, model_file=None, use_cuda=False):
        self.use_cuda = use_cuda
        if model_file is not None:
            # load everything from file
            self.load(model_file, use_cuda)
        else:
            # build model from scratch
            self.args = args
            self.model = None if args['dict_only'] else Seq2SeqModel(args, emb_matrix=emb_matrix, use_cuda=use_cuda)
            self.vocab = vocab
            # dict-based components
            self.word_dict = dict()
            self.composite_dict = dict()
        if not self.args['dict_only']:
            if self.args.get('edit', False):
                self.crit = MixLoss(self.vocab['char'].size, self.args['alpha'])
            else:
                self.crit = SequenceLoss(self.vocab['char'].size)
            self.parameters = [p for p in self.model.parameters() if p.requires_grad]
            if use_cuda:
                self.model.cuda()
                self.crit.cuda()
            else:
                self.model.cpu()
                self.crit.cpu()
            self.optimizer = get_optimizer(self.args['optim'], self.parameters, self.args['lr'])

    def update(self, batch, eval=False):
        inputs, orig_idx = unpack_lemma_batch(batch, self.use_cuda)
        src, src_mask, tgt_in, tgt_out, pos, edits = inputs

        if eval:
            self.model.eval()
        else:
            self.model.train()
            self.optimizer.zero_grad()
        log_probs, edit_logits = self.model(src, src_mask, tgt_in, pos)
        if self.args.get('edit', False):
            assert edit_logits is not None
            loss = self.crit(log_probs.view(-1, self.vocab['char'].size), tgt_out.view(-1), \
                             edit_logits, edits)
        else:
            loss = self.crit(log_probs.view(-1, self.vocab['char'].size), tgt_out.view(-1))
        loss_val = loss.data.item()
        if eval:
            return loss_val

        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.args['max_grad_norm'])
        self.optimizer.step()
        return loss_val

    def predict(self, batch, beam_size=1):
        inputs, orig_idx = unpack_lemma_batch(batch, self.use_cuda)
        src, src_mask, tgt, tgt_mask, pos, edits = inputs

        self.model.eval()
        batch_size = src.size(0)
        preds, edit_logits = self.model.predict(src, src_mask, pos=pos, beam_size=beam_size)
        pred_seqs = [self.vocab['char'].unmap(ids) for ids in preds]  # unmap to tokens
        pred_seqs = prune_decoded_seqs(pred_seqs)
        pred_tokens = ["".join(seq) for seq in pred_seqs]  # join chars to be tokens
        pred_tokens = unsort(pred_tokens, orig_idx)
        if self.args.get('edit', False):
            assert edit_logits is not None
            edits = np.argmax(edit_logits.data.cpu().numpy(), axis=1).reshape([batch_size]).tolist()
            edits = unsort(edits, orig_idx)
        else:
            edits = None
        return pred_tokens, edits

    def postprocess(self, words, preds, edits=None):
        """ Postprocess, mainly for handing edits. """
        assert len(words) == len(preds), "Lemma predictions must have same length as words."
        edited = []
        if self.args.get('edit', False):
            assert edits is not None and len(words) == len(edits)
            for w, p, e in zip(words, preds, edits):
                lem = edit_word(w, p, e)
                edited += [lem]
        else:
            edited = preds  # do not edit
        # final sanity check
        assert len(edited) == len(words)
        final = []
        for lem, w in zip(edited, words):
            if len(lem) == 0 or UNK in lem:
                final += [w]  # invalid prediction, fall back to word
            else:
                final += [lem]
        return final

    def update_lr(self, new_lr):
        change_lr(self.optimizer, new_lr)

    def train_dict(self, triples):
        """ Train a dict lemmatizer given training (word, pos, lemma) triples. """
        # accumulate counter
        ctr = Counter()
        ctr.update([(p[0], p[1], p[2]) for p in triples])
        # find the most frequent mappings
        for p, _ in ctr.most_common():
            w, pos, l = p
            if (w, pos) not in self.composite_dict:
                self.composite_dict[(w, pos)] = l
            if w not in self.word_dict:
                self.word_dict[w] = l
        return

    def predict_dict(self, pairs):
        """ Predict a list of lemmas using the dict model given (word, pos) pairs. """
        lemmas = []
        for p in pairs:
            w, pos = p
            if (w, pos) in self.composite_dict:
                lemmas += [self.composite_dict[(w, pos)]]
            elif w in self.word_dict:
                lemmas += [self.word_dict[w]]
            else:
                lemmas += [w]
        return lemmas

    def skip_seq2seq(self, pairs):
        """ Determine if we can skip the seq2seq module when ensembling with the frequency lexicon. """

        skip = []
        for p in pairs:
            w, pos = p
            if (w, pos) in self.composite_dict:
                skip.append(True)
            elif w in self.word_dict:
                skip.append(True)
            else:
                skip.append(False)
        return skip

    def ensemble(self, pairs, other_preds):
        """ Ensemble the dict with statistical model predictions. """
        lemmas = []
        assert len(pairs) == len(other_preds)
        for p, pred in zip(pairs, other_preds):
            w, pos = p
            if (w, pos) in self.composite_dict:
                lemma = self.composite_dict[(w, pos)]
            elif w in self.word_dict:
                lemma = self.word_dict[w]
            else:
                lemma = pred
            if lemma is None:
                lemma = w
            lemmas.append(lemma)
        return lemmas

    def save(self, filename):
        params = {
            'model': self.model.state_dict() if self.model is not None else None,
            'dicts': (self.word_dict, self.composite_dict),
            'vocab': self.vocab.state_dict(),
            'config': self.args
        }
        try:
            torch.save(params, filename)
        except BaseException:
            raise

    def load(self, filename, use_cuda=False):
        try:
            checkpoint = torch.load(filename, lambda storage, loc: storage)
        except BaseException:
            raise
        self.args = checkpoint['config']
        self.word_dict, self.composite_dict = checkpoint['dicts']
        if not self.args['dict_only']:
            self.model = Seq2SeqModel(self.args, use_cuda=use_cuda)
            self.model.load_state_dict(checkpoint['model'])
        else:
            self.model = None
        self.vocab = MultiVocab.load_state_dict(checkpoint['vocab'])


def get_identity_lemma_model():
    args = {
        'data_dir': '',
        'train_file': '',
        'eval_file': '',
        'output_file': '',
        'gold_file': '',
        'mode': 'predict',
        'lang': '',
        'batch_size': 5000,
        'seed': 1234
    }

    return args


def get_lemma_model(cache_dir, language, use_gpu):
    args = {
        'train_file': '',
        'eval_file': '',
        'output_file': '',
        'gold_file': '',
        'mode': 'predict',
        'lang': '',
        'ensemble_dict': True,
        'dict_only': False,
        'hidden_dim': 200,
        'emb_dim': 50,
        'num_layers': 1,
        'emb_dropout': 0.5,
        'dropout': 0.5,
        'max_dec_len': 50,
        'beam_size': 1,
        'attn_type': 'soft',
        'pos_dim': 50,
        'pos_dropout': 0.5,
        'edit': True,
        'num_edit': len(EDIT_TO_ID),
        'alpha': 1.0,
        'pos': True,
        'sample_train': 1.0,
        'optim': 'adam',
        'lr': 1e-3,
        'lr_decay': 0.9,
        'decay_epoch': 30,
        'num_epoch': 15,
        'batch_size': 5000,
        'max_grad_norm': 5.0,
        'log_step': 20,
        'seed': 1234
    }
    # load model
    model_file = os.path.join(cache_dir, '{}/{}_lemmatizer.pt'.format(language, language))
    args['data_dir'] = os.path.join(cache_dir, language)
    args['model_dir'] = os.path.join(cache_dir, language)
    trainer = Trainer(model_file=model_file, use_cuda=use_gpu)
    loaded_args, vocab = trainer.args, trainer.vocab

    for k in args:
        if k.endswith('_dir') or k.endswith('_file'):
            loaded_args[k] = args[k]

    return trainer, args, loaded_args, vocab


class LemmaWrapper:
    # adapted from stanza
    def __init__(self, config, treebank_name, use_gpu):
        self.config = config
        self.treebank_name = treebank_name
        if self.treebank_name in ['UD_Old_French-SRCMF', 'UD_Vietnamese-VTB']:
            self.args = get_identity_lemma_model()
        else:
            self.model, self.args, self.loaded_args, self.vocab = get_lemma_model(self.config._cache_dir,
                                                                                  treebank2lang[treebank_name], use_gpu)
        print('Loading lemmatizer for {}'.format(treebank2lang[treebank_name]))

    def predict(self, tagged_doc, obmit_tag):
        if self.treebank_name not in ['UD_Old_French-SRCMF', 'UD_Vietnamese-VTB']:
            vocab = self.vocab
            # load data
            batch = LemmaDataLoader(tagged_doc, self.args['batch_size'], self.loaded_args, vocab=vocab,
                                    evaluation=True)

            # skip eval if dev data does not exist
            if len(batch) == 0:
                print("Skip evaluation because no dev data is available...")
                print("Lemma score:")
                print("{} ".format(self.args['lang']))
                sys.exit(0)
            predict_dict_input = []
            for sentence in batch.doc:
                for t in sentence[TOKENS]:
                    if type(t[ID]) == int or len(t[ID]) == 1:
                        predict_dict_input.append([t[TEXT], t[UPOS] if UPOS in t else None])
                    else:
                        for w in t[EXPANDED]:
                            predict_dict_input.append([w[TEXT], w[UPOS] if UPOS in w else None])

            preds = []
            edits = []
            for i, b in enumerate(batch):
                ps, es = self.model.predict(b, self.args['beam_size'])
                preds += ps
                if es is not None:
                    edits += es

            postprocess_input = [w[0] for w in predict_dict_input]
            preds = self.model.postprocess(
                postprocess_input,
                preds,
                edits=edits)

            preds = self.model.ensemble(
                predict_dict_input, preds)

            # write to file and score
            lemmatized_doc = set_lemma(batch.doc, preds, obmit_tag)
        else:
            document = tagged_doc
            batch = LemmaDataLoader(document, self.args['batch_size'], self.args, evaluation=True,
                                    conll_only=True)

            # use identity mapping for prediction
            preds = [t[TEXT] for sentence in document for t in sentence[TOKENS] if
                     type(t[ID]) == int or len(t[ID]) == 1]

            # write to file and score
            lemmatized_doc = set_lemma(batch.doc, preds, obmit_tag)
        return lemmatized_doc
