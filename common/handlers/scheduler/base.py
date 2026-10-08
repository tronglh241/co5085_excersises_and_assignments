from common.engine.engine import Events


class Scheduler:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def attach(self, trainer, event=Events.EPOCH_COMPLETED):
        trainer.add_event_handler(event, self)

    def __call__(self, engine):
        raise NotImplementedError
