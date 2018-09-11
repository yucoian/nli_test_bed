from utils.utils import dotdict

config = dotdict({
    'model': 'nli',
    'encoder': 'transformer_inter_attention',
    'aggregator': 'linear_aggregate',
    'dataset': 'snli',
    'tokenize': False,
    'word_vectors': 'glove.6B.100d',
    'vector_cache': '.vector_cache/input_vectors.pt',
    'save_path': 'results',
    'siamese': False, # TODO: not implemented yet
    'seed': 42,
    'gpu': 0,
    'epochs': 10,
    'lr': 0.001,
    'batch_size': 16,
    'd_embed': 100,
    'd_proj': 300,
    'n_layers': 1,
    'n_cells': 1,
    'd_hidden': 100,
    'd_transformer': 100,
    'd_ff_transformer': 2048,
    'h_transformer': 5,
    'dp_ratio': 0.2, # TODO: remove because of dropout_pe
    'print_every_n_batch': 100,
    'eval_every_n_batch': 100,
    'criterion': 'cross_entropy_loss',
    'optimizer': 'adam',
    'loss_compute': 'simple_loss_compute',
    'train_embed': True,
    'apply_weight_embed': True,
    'positional_encoding': True,
    'dropout_pe': 0.2,
    'max_len': 500, # TODO: not implemented yet
    'eps': 1e-6,
})

"""
'model': 'nli',
    'encoder': 'lstm',
    'aggregator': 'linear_aggregate',
    'dataset': 'snli',
    'tokenize': False,
    'word_vectors': 'glove.6B.100d',
    'vector_cache': '.vector_cache/input_vectors.pt',
    'seed': 42,
    'gpu': 0,
    'epochs': 10,
    'lr': 0.001,
    'batch_size': 16,
    'd_embed': 100,
    'd_proj': 300,
    'n_layers': 1,
    'n_cells': 1,
    'd_hidden': 300,
    'dp_ratio': 0.2,
    'print_every_n_batch': 100,
    'criterion': 'cross_entropy_loss',
    'optimizer': 'adam',
    'loss_compute': 'simple_loss_compute',
    'train_embed': True,
    'apply_weight_embed': True,
    'positional_encoding': False,
    'dropout_pe': 0.2,
    'max_len': 500, # TODO: not implemented yet
"""