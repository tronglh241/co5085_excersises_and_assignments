import os
from datetime import datetime

from torch.utils.tensorboard import SummaryWriter

from common.engine.engine import Events


class TensorBoardLogger:
    def __init__(self, log_dir):
        self.log_dir = os.path.join(log_dir, datetime.now().strftime('%y%m%d%H%M%S'))
        self.writer = SummaryWriter(self.log_dir)

    def attach(self, engine, prefix='', optimizer=None):
        engine.add_event_handler(Events.EPOCH_COMPLETED, self._log_result, prefix)

        if optimizer is not None:
            engine.add_event_handler(Events.EPOCH_COMPLETED, self._log_lr, optimizer, prefix)

        engine.add_event_handler(Events.COMPLETED, self._flush)

    def _log_result(self, engine, prefix):
        for metric, value in (engine.result or {}).items():
            if metric == 'n':  # Number of samples
                continue

            if hasattr(value, 'numel') and value.numel() > 1:
                for i, v in enumerate(value):
                    tag = f'{prefix}/{metric}/{i}'
                    self.writer.add_scalar(tag, float(v), engine.state['epoch'])
            else:
                tag = f'{prefix}/{metric}'
                self.writer.add_scalar(tag, float(value), engine.state['epoch'])

    def _log_lr(self, engine, optimizer, prefix):
        tag = f'{prefix}/lr' if prefix else 'lr'
        groups = optimizer.param_groups

        if len(groups) == 1:
            self.writer.add_scalar(tag, groups[0]['lr'], engine.state['epoch'])
        else:
            for i, pg in enumerate(groups):
                self.writer.add_scalar(f'{tag}/group_{i}', pg['lr'], engine.state['epoch'])

    def _flush(self, engine):
        self.writer.flush()
