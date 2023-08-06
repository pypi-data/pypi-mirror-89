# -*- coding: utf-8 -*-
# import sys
#
# sys.path.append('./')
# sys.path.append('./phonlp')
from phonlp.models.common import utils as util
from tqdm import tqdm
from phonlp.models.common.chuliu_edmonds import chuliu_edmonds_one_root
# from phonlp.models.jointmodel3task.model import *
import torch
from phonlp.model_eval import JointModel
from phonlp.models.ner.vocab import MultiVocab
from transformers import AutoConfig, AutoTokenizer
import gdown
import os


def download(model_folder_path, url="https://drive.google.com/uc?id=1ZFfyppGc4QKdeGve1kvpj44GTlM9Rl-H"):
    gdown.download(url, model_folder_path)

def load(model_folder_path='./'):
    #model_file = "/home/vinai/Documents/PhoToolkit/phonlp/models/save_model/VnDTv1.1_jointmodel.pt"
    if model_folder_path[len(model_folder_path) - 1] == '/':
        model_file = model_folder_path + "VnDTv1.1_jointmodel.pt"
    else:
        model_file = model_folder_path + "/VnDTv1.1_jointmodel.pt"
    tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base', use_fast=False)
    config_phobert = AutoConfig.from_pretrained('vinai/phobert-base', output_hidden_states=True)
    print("Loading model from: {}".format(model_file))
    checkpoint = torch.load(model_file, lambda storage, loc: storage)
    args = checkpoint['config']
    vocab = MultiVocab.load_state_dict(checkpoint['vocab'])
    # load model
    model = JointModel(args, vocab, config_phobert, tokenizer)
    model.load_state_dict(checkpoint['model'], strict=False)
    if torch.cuda.is_available() == False:
        model.to(torch.device('cpu'))
    else:
        model.to(torch.device('cuda'))
    model.eval()
    return model

if __name__ == '__main__':
    download("./")
    model = load("./")
    text = "Tôi tên là Thế_Linh ."
    output = model.annotate(text=text)
    model.print_out(output)

#     annotate(text=text, type='sentence')#input_file='input.txt', output_file='output.txt')
