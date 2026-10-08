import os
from datetime import datetime

from torch.utils.tensorboard import SummaryWriter

from common.engine.engine import Events


class TensorBoardLogger:
    def __init__(self, log_dir):
        self.log_dir = os.path.join(log_dir, datetime.now().strftime('%y%m%d%H%M%S'))
        self.writer = SummaryWriter(self.log_dir)

    def attach(self, trainer, evaluators):
        trainer.add_event_handler(Events.ITERATION_COMPLETED, self._log_train_loss)

        for name, evaluator in evaluators.items():
            evaluator.add_event_handler(Events.EPOCH_COMPLETED, self._log_eval_metrics, name)

        trainer.add_event_handler(Events.COMPLETED, self._close)

    def _log_train_loss(self, engine):
        self.writer.add_scalar('training/loss', engine.output['loss'], engine.state['iteration'])

    def _log_eval_metrics(self, engine, name):
        for metric, value in engine.result.items():
            if metric == 'n':  # Number of samples
                continue

            if hasattr(value, 'numel') and value.numel() > 1:
                for i, v in enumerate(value):
                    self.writer.add_scalar(f'{name}/{metric}/{i}', float(v), engine.state['epoch'])
            else:
                self.writer.add_scalar(f'{name}/{metric}', float(value), engine.state['epoch'])

    def _close(self, engine):
        self.writer.close()
