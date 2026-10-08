import argparse
import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parents[1])
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import torch

from common.config.config import CfgNode
from common.config.validate import validate_eval_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args()

    cfg = CfgNode.load(args.config)
    validate_eval_config(cfg)

    if 'metrics' in cfg:
        for name, metric in cfg.metrics.items():
            metric.attach(cfg.evaluator, name)

    cfg.loader.attach(cfg.evaluator, {'model': cfg.model})

    if 'logging' in cfg:
        if 'tensorboard' in cfg.logging:
            cfg.logging.tensorboard.attach(None, {'eval': cfg.evaluator})

        if 'tqdm' in cfg.logging:
            cfg.logging.tqdm.attach(None, {'eval': cfg.evaluator})

    result = cfg.evaluator.run()

    print(f'n: {result["n"]}')
    for name, value in result.items():
        if name == 'n':
            continue
        if torch.is_tensor(value) and value.numel() > 1:
            print(f'{name}:')
            print(value)
        else:
            number = value.item() if torch.is_tensor(value) else value
            print(f'{name}: {number:.4f}' if isinstance(number, float) else f'{name}: {number}')
