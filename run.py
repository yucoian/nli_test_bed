import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as O
import matplotlib.pyplot as plt
from tensorboardX import SummaryWriter

from utils.train_utils import (get_device_info, set_seed, run_epoch, save_model, 
    restore_model)
from utils.utils import *
from utils.text_utils import text_to_var

def main():
    # ----- get config -----
    config = parse_args_get_config()

    # ----- logger -----
    logger = SummaryWriter(log_dir=config.log_path + "/" + config.run_name)
    for c, c_value in config.items(): logger.add_text(c, str(c_value))

    # ----- set seed -----
    set_seed(config)

    # ----- get device -----
    device, n_gpu = get_device_info(config)
    config.device = device

    # ----- load data object -----
    print("Loading data")
    data = get_data(config)
    config['n_updates_total']=len(data.train_iter) * config.epochs

    # ----- create or load model -----
    print("Loading model")
    model = get_model(config, data.vocab)
    if config.restore_model:
        print("restoring")
        restore_model(model, config.restore_path, device)
    model.to(device)
    pytorch_total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print("Total params: ", pytorch_total_params)
    print(model)

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

            # ----- train -----
            model.train()
            run_epoch(logger, config, i, data, data.train_iter, model, 
                loss_compute, device, mode='train', save_misclassified=False)

            # ----- dev -----
            model.eval()
            with torch.no_grad():
                dev_acc, dev_loss = run_epoch(logger, config, i, data, data.dev_iter, 
                    model, loss_compute_dev, device, mode='dev', save_misclassified=False)
                if dev_acc > best_dev_acc:
                    best_dev_acc = dev_acc
                    if config.save_model:
                        save_model(model, config, dev_acc, i)
            
            # ----- test -----
            with torch.no_grad():
                run_epoch(logger, config, i, data, data.test_iter, 
                    model, loss_compute_dev, device, mode='test', save_misclassified=True)

    
    # ----- test mode -----
    elif config.mode == 'test':
        print("Testing")
        model.eval()
        with torch.no_grad():
            test_acc, test_loss = run_epoch(logger, config, 0, data, 
                data.test_iter,model, loss_compute_dev, device, mode='test', save_misclassified=True)
            print("Test loss: ", test_loss)
            print("Test acc: ", test_acc)
    

    # ----- interactive mode -----
    elif config.mode == 'interactive':
        print("Interactive")
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
            
            model.draw(sent_p, sent_h)

    logger.close()


if __name__ == "__main__":
    main()