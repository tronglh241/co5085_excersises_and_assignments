from collections.abc import Mapping
from typing import Any

from ignite.handlers.param_scheduler import ReduceLROnPlateauScheduler


class SerializableReduceLROnPlateauScheduler(ReduceLROnPlateauScheduler):
    """ReduceLROnPlateauScheduler with a torch.save-able state_dict.

    Upstream ``__init__`` monkey-patches the wrapped torch scheduler instance
    (``self.scheduler._reduce_lr = self._reduce_lr``), and torch's
    ``ReduceLROnPlateau.state_dict()`` dumps every ``__dict__`` entry except
    ``optimizer`` — so the saved state contains a bound method, which pickle
    cannot serialize (it references the wrapper, optimizer, trainer engine).

    This subclass drops that entry on save and re-attaches the live bound
    method on load. All real scheduler state (best, num_bad_epochs, patience,
    factor, ...) is plain data and is preserved, so runtime LR behavior is
    identical to the parent class.
    """

    def state_dict(self) -> dict[str, Any]:
        state = super().state_dict()
        # super() shallow-copies the nested torch-scheduler dict, so popping
        # here never mutates the live scheduler.
        state["scheduler"].pop("_reduce_lr", None)
        return state

    def load_state_dict(self, state_dict: Mapping) -> None:
        super().load_state_dict(state_dict)
        # Torch's loader is __dict__.update-lenient: the absent _reduce_lr key
        # is preserved, but re-attach explicitly to keep the invariant obvious.
        self.scheduler._reduce_lr = self._reduce_lr
