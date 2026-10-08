import argparse
import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parents[1])
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

from common.config.config import CfgNode
from common.config.validate import validate_train_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args()

    cfg = CfgNode.load(args.config)
    validate_train_config(cfg)

    if 'loader' in cfg:
        cfg.loader.attach(cfg.trainer, cfg)

    if 'evaluators' in cfg:
        if 'metrics' in cfg:
            for key in cfg.evaluators:
                for name, metric in cfg.metrics.items():
                    metric.attach(cfg.evaluators[key], name)

        def evaluate(engine):
            for key in cfg.evaluators:
                cfg.evaluators[key].run()

        cfg.trainer.on_epoch_completed(evaluate)

    if 'logging' in cfg:
        if 'tensorboard' in cfg.logging:
            cfg.logging.tensorboard.attach(cfg.trainer, cfg.evaluators)

        if 'tqdm' in cfg.logging:
            cfg.logging.tqdm.attach(cfg.trainer, cfg.evaluators)

    if 'checkpoint' in cfg:
        if 'best' in cfg.checkpoint:
            cfg.checkpoint.best.attach(cfg.trainer, cfg)

        if 'backup' in cfg.checkpoint:
            cfg.checkpoint.backup.attach(cfg.trainer, cfg)

    if 'scheduler' in cfg:
        cfg.scheduler.attach(cfg.trainer)

    if 'early_stopping' in cfg:
        cfg.early_stopping.attach(cfg.trainer)

    cfg.trainer.run()
