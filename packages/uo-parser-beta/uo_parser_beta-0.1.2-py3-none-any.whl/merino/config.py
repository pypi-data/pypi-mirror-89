import os
import torch
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


class Config:
    def __init__(self):
        self.xlmr_model_name = 'xlm-roberta-base'
        self.xlmr_dropout = 0.3
        self.hidden_num = 300
        self.linear_dropout = 0.1
        self.linear_bias = 1
        self.linear_activation = 'relu'
        self.working_dir = os.path.dirname(os.path.realpath(__file__))
        self.lowercase = False


# configuration
config = Config()
