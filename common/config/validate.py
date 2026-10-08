from torch import nn
from torch.utils.data import DataLoader

from common.engine.evaluator import Evaluator
from common.engine.trainer import Trainer
from common.handlers.early_stopping import EarlyStopping
from common.handlers.logging.tensorboard import TensorBoardLogger
from common.handlers.logging.tqdm_logger import TQDMLogger
from common.handlers.scheduler.base import Scheduler


def validate_train_config(cfg):
    for key in ('data', 'model', 'optimizer', 'loss_fn', 'trainer'):
        assert key in cfg, f"config missing required key: '{key}'"

    for split in ('train', 'train_eval', 'valid'):
        assert split in cfg.data, f"config missing data split: 'data.{split}'"
        assert isinstance(cfg.data[split], DataLoader), f'data.{split} must be a DataLoader'

    assert isinstance(cfg.model, nn.Module), 'model must be an nn.Module'
    assert isinstance(cfg.trainer, Trainer), 'trainer must be a Trainer'

    if 'evaluators' in cfg:
        for key in cfg.evaluators:
            assert isinstance(cfg.evaluators[key], Evaluator), f'evaluators.{key} must be an Evaluator'

        if 'metrics' in cfg:
            assert len(cfg.metrics) > 0, 'metrics must be non-empty'
            for name, metric in cfg.metrics.items():
                assert callable(getattr(metric, 'attach', None)), f"metric '{name}' must define attach(evaluator, name)"
    elif 'metrics' in cfg:
        assert False, "config has 'metrics' but no 'evaluators' to attach them to"

    if 'scheduler' in cfg or 'early_stopping' in cfg:
        assert 'evaluators' in cfg and 'valid' in cfg.evaluators, \
            "scheduler/early_stopping need 'evaluators.valid' for the monitored metric"

    if 'scheduler' in cfg:
        assert isinstance(cfg.scheduler, Scheduler), 'scheduler must be a Scheduler'

    if 'early_stopping' in cfg:
        assert isinstance(cfg.early_stopping, EarlyStopping), 'early_stopping must be an EarlyStopping'

    if 'logging' in cfg:
        has_tb = 'tensorboard' in cfg.logging
        has_tqdm = 'tqdm' in cfg.logging

        assert has_tb or has_tqdm, "config logging block must define 'tensorboard' and/or 'tqdm'"

        if 'tensorboard' in cfg.logging:
            logger = cfg.logging.tensorboard
            assert isinstance(logger, TensorBoardLogger), 'logging.tensorboard must be a TensorBoardLogger'
            assert isinstance(logger.log_dir, str), 'logging.tensorboard log_dir must be a string'

        if 'tqdm' in cfg.logging:
            assert isinstance(cfg.logging.tqdm, TQDMLogger), 'logging.tqdm must be a TQDMLogger'
