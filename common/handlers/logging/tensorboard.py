import os
from datetime import datetime

from torch.utils.tensorboard import SummaryWriter

from common.engine.engine import Events


class TensorBoardLogger:
    def __init__(self, log_dir):
        self.log_dir = os.path.join(log_dir, datetime.now().strftime('%y%m%d%H%M%S'))
        self.writer = SummaryWriter(self.log_dir)

    def attach(self, engine, prefix=''):
        engine.add_event_handler(Events.ITERATION_COMPLETED, self._log_output, prefix)
        engine.add_event_handler(Events.EPOCH_COMPLETED, self._log_result, prefix)
        engine.add_event_handler(Events.COMPLETED, self._flush)

    def _log_output(self, engine, prefix):
        tag = f'{prefix}/loss' if prefix else 'loss'

        for key, value in (engine.output or {}).items():
            if key == 'loss':
                self.writer.add_scalar(tag, float(value), engine.state['iteration'])

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

    def _flush(self, engine):
        self.writer.flush()
