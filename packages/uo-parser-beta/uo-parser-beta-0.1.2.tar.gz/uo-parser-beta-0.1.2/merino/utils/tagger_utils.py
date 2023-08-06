import os
import json
from copy import deepcopy
from .conll import *


def write_to_conllu_file(conllu_doc, conllu_pred_fpath):
    out_doc = []
    for sent_id, sent in conllu_doc.items():
        out_sent = []
        num_words = len(sent.keys()) - 1
        for word_id in range(1, num_words + 1):
            word = sent[word_id]
            out_sent.append('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                word_id, word['text'], word['lemma'],
                '_', '_', '_', f'{word_id - 1}', '_', '_', '_'
            ))

        mwts = [(m['text'], m['start'], m['end']) for m in sent['mwts']]
        mwts.sort(key=lambda x: -x[1])
        for mwt in mwts:
            text, start, end = mwt
            out_sent = out_sent[:start] + [
                '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                    f'{start}-{end}', text, '_',
                    '_', '_', '_', '_', '_', '_', '_'
                )
            ] + out_sent[start:]
        out_doc.append('\n'.join(out_sent))

    with open(conllu_pred_fpath, 'w') as f:
        f.write('\n\n'.join(out_doc) + '\n')


def get_examples_from_conllu(wordpiece_splitter, max_input_length, tokenized_doc):
    examples = []
    conllu_doc = {}
    skip_num = 0
    for sid, sentence in enumerate(tokenized_doc):
        new_ex = {
            'sent_index': sid,
            'mwts': [],
            'words': [],
            'word_ids': [],
            LEMMA: [],
            UPOS: [],
            XPOS: [],
            FEATS: [],
            HEAD: [],
            DEPREL: []
        }
        conllu_doc[sid] = {
            'mwts': []
        }
        for token in sentence[TOKENS]:
            if type(token[ID]) == tuple and len(token[ID]) == 2:
                new_ex['mwts'].append({
                    'text': token[TEXT],
                    'start': token[ID][0],
                    'end': token[ID][1]
                })
                conllu_doc[sid]['mwts'].append({
                    'text': token[TEXT],
                    'start': token[ID][0],
                    'end': token[ID][1]
                })
                for word in token[EXPANDED]:
                    src_text = word[TEXT]

                    edit_operation = '0'

                    upos = '_'
                    xpos = '_'
                    feats = '_'

                    head = 0
                    deprel = '_'

                    # for conllu_doc, take all
                    conllu_doc[sid][word[ID]] = {
                        'id': word[ID],
                        'text': src_text
                    }

                    # add info to example
                    new_ex['word_ids'].append(word[ID])
                    new_ex['words'].append(src_text)
                    new_ex[LEMMA].append(edit_operation)
                    new_ex[UPOS].append(upos)
                    new_ex[XPOS].append(xpos)
                    new_ex[FEATS].append(feats)

                    new_ex[HEAD].append(head)
                    new_ex[DEPREL].append(deprel)
            else:
                src_text = token[TEXT]

                edit_operation = '0'

                upos = '_'
                xpos = '_'
                feats = '_'

                head = 0
                deprel = '_'

                # for conllu_doc, take all
                conllu_doc[sid][token[ID]] = {
                    'id': token[ID],
                    'text': src_text
                }

                # add info to example
                new_ex['word_ids'].append(token[ID])
                new_ex['words'].append(src_text)
                new_ex[LEMMA].append(edit_operation)
                new_ex[UPOS].append(upos)
                new_ex[XPOS].append(xpos)
                new_ex[FEATS].append(feats)

                new_ex[HEAD].append(head)
                new_ex[DEPREL].append(deprel)

        pieces = [[p for p in wordpiece_splitter.tokenize(w) if p != '▁'] for w in new_ex['words']]
        flat_pieces = [p for ps in pieces for p in ps]
        if len(flat_pieces) > max_input_length - 2:
            skip_num += 1
            continue
        else:
            examples.append(new_ex)

    return examples, conllu_doc
