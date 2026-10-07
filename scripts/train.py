import argparse

from common.config.config import CfgNode
from common.config.validate import validate_train_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args()

    cfg = CfgNode.load(args.config)
    validate_train_config(cfg)

    for name, metric in cfg.metrics.items():
        metric.attach(cfg.evaluators.train, name)
        metric.attach(cfg.evaluators.valid, name)

    def evaluate(engine):
        cfg.evaluators.train.run()
        cfg.evaluators.valid.run()

    cfg.trainer.on_epoch_completed(evaluate)

    if 'logging' in cfg:
        if 'tensorboard' in cfg.logging:
            cfg.logging.tensorboard.attach(cfg.trainer, cfg.evaluators)

        if 'tqdm' in cfg.logging:
            cfg.logging.tqdm.attach(cfg.trainer, cfg.evaluators)

    cfg.trainer.run()
