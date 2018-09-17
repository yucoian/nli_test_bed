import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as O
import matplotlib.pyplot as plt

# from config import config
from utils.train_utils import get_device_info, set_seed, run_epoch, save_model
from utils.utils import *
from utils.text_utils import text_to_var

def main():
    # ----- get config -----
    config = parse_args_get_config()

    # ----- set seed -----
    set_seed(config)

    # ----- get device -----
    device, n_gpu = get_device_info(config)
    config.device = device

    # ----- load data object -----
    print("Loading data")
    data = get_data(config)

    # ----- create or load model -----
    print("Loading model")
    model = get_model(config, data.vocab)
    model.to(device)

    # ----- create criterion -----
    print("Loading criterion")
    criterion = get_criterion(config)

    # ----- create optimizer -----
    print("Loading optimizer")
    optimizer = get_optimizer(config, model)

    # ----- get loss compute function -----
    print("Loading loss compute function")
    loss_compute = get_loss_compute(config, criterion, optimizer)
    loss_compute_dev = get_loss_compute(config, criterion, None)

    # ----- train mode -----
    if config.mode == 'train':
        
        print("Training")
        best_dev_acc = -1
        for i in range(config.epochs):
            model.train()
            run_epoch(config, i, data.train_iter, model, loss_compute, device, mode='train')

            # ----- dev -----
            model.eval()
            with torch.no_grad():
                dev_acc = run_epoch(i, data.dev_iter, model, loss_compute_dev, device, mode='eval')
                if dev_acc > best_dev_acc:
                    best_dev_acc = dev_acc
                    if config.save_model:
                        save_model(model, config, dev_acc, i)
                

    
    # ----- test mode -----
    elif config.mode == 'test':
        model.eval()
        with torch.no_grad():
            test_acc = run_epoch(config, 0, data.test_iter, model, loss_compute_dev, device, mode='test')
    

    # ----- visualization mode -----
    elif config.mode == 'visualize':
        model.eval()
        while True:
            premise = input("premise > ")
            hypothesis = input("hypothesis > ")

            if not premise or not hypothesis:
                print("Please enter premise and hypothesis")
                continue
            
            premise_var = text_to_var(premise, data.TEXT, config)
            hypothesis_var = text_to_var(hypothesis, data.TEXT, config)
            mbatch = dotdict({
                'premise': premise_var,
                'hypothesis': hypothesis_var,
            })

            sent_p = premise.split()
            sent_h = hypothesis.split()

            scores = model(mbatch)

            model.encode_p.draw_attentions(sent_p, sent_h)
            model.encode_h.draw_attentions(sent_h, sent_p)


            

            

if __name__ == "__main__":
    main()