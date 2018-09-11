import torch
import torch.nn as nn

from .aggregators import aggregators

class Aggregator(nn.Module):
    def __init__(self, config):
        super(Aggregator, self).__init__()
        if not config.aggregator:
            raise NotImplementedError("'aggregator' not defined in config")
        
        if config.aggregator not in aggregators:
            raise NotImplementedError(f"aggregator '{config.aggregator}' not implemented")
        
        self.aggregator = aggregators[config.aggregator](config)
    
    def forward(self, x, y):
        """
        x (batch_size, d_hidden)
        y (batch_size, d_hidden)
        output (batch_size, d_out)
        """
        return self.aggregator(torch.cat([x, y], 1))