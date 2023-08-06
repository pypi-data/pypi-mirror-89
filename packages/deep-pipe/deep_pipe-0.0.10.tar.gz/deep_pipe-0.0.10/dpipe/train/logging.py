import os
from collections import defaultdict
from functools import partial
from typing import Sequence, Union

import numpy as np

from dpipe.io import PathLike
from dpipe.im.utils import zip_equal

__all__ = 'Logger', 'ConsoleLogger', 'TBLogger', 'NamedTBLogger',


def log_vector(logger, tag: str, vector, step: int):
    for i, value in enumerate(vector):
        logger.log_scalar(tag=tag + f'/{i}', value=value, step=step)


def log_scalar_or_vector(logger, tag, value: np.ndarray, step):
    value = np.asarray(value).flatten()
    if value.size > 1:
        log_vector(logger, tag, value, step)
    else:
        logger.log_scalar(tag, value, step)


def make_log_vector(logger, tag: str, first_step: int = 0) -> callable:
    def log(tag, value, step):
        log_vector(logger, tag, value, step)

    return logger._make_log(tag, first_step, log)


def group_dicts(dicts):
    groups = defaultdict(list)
    for entry in dicts:
        for name, value in entry.items():
            groups[name].append(value)

    return dict(groups)


class Logger:
    """Interface for logging during training."""

    def _dict(self, prefix, d, step):
        for name, value in d.items():
            self.value(f'{prefix}{name}', value, step)

    def train(self, train_losses: Sequence, step: int):
        """Log the ``train_losses`` at current ``step``."""
        raise NotImplementedError

    def value(self, name: str, value, step: int):
        """Log a single ``value``."""
        raise NotImplementedError

    def policies(self, policies: dict, step: int):
        """Log values coming from `ValuePolicy` objects."""
        self._dict('policies/', policies, step)

    def metrics(self, metrics: dict, step: int):
        """Log the metrics returned by the validation function during training."""
        self._dict('val/metrics/', metrics, step)


class ConsoleLogger(Logger):
    """A logger that writes to to stdout."""

    def value(self, name, value, step):
        print(f'{step:>05}: {name}: {value}', flush=True)

    def train(self, train_losses: Sequence[Union[dict, tuple, float]], step):
        text = ''
        if train_losses and isinstance(train_losses[0], dict):
            for name, values in group_dicts(train_losses).items():
                text += f'{name}: {np.mean(values)} '

        else:
            text += str(np.mean(train_losses, axis=0))

        self.value('Train loss', text, step)

    def policies(self, policies: dict, step: int):
        self._dict('Policies: ', policies, step)

    def metrics(self, metrics: dict, step: int):
        self._dict('Metrics: ', metrics, step)


class TBLogger(Logger):
    """A logger that writes to a tensorboard log file located at ``log_path``."""

    def __init__(self, log_path: PathLike):
        import tensorboard_easy
        self.logger = tensorboard_easy.Logger(log_path)

    def train(self, train_losses: Sequence[Union[dict, tuple, float]], step):
        if train_losses and isinstance(train_losses[0], dict):
            for name, values in group_dicts(train_losses).items():
                self.value(f'train/loss/{name}', np.mean(values), step)

        else:
            self.value('train/loss', np.mean(train_losses, axis=0), step)

    def value(self, name, value, step):
        dirname, base = os.path.split(name)

        count = base.count('__')
        if count > 1:
            raise ValueError(f'The tag name must contain at most one magic delimiter (__): {base}.')
        if count:
            base, kind = base.split('__')
        else:
            kind = 'scalar'

        name = os.path.join(dirname, base)

        if kind == 'vector':
            log = partial(log_vector, self.logger)
        else:
            log = getattr(self.logger, f'log_{kind}')
        log(name, np.asarray(value), step)

    def __getattr__(self, item):
        return getattr(self.logger, item)


class NamedTBLogger(TBLogger):
    """
    A logger that writes multiple train losses to a tensorboard log file located at ``log_path``.

    Each loss is assigned to a corresponding tag name from ``loss_names``.
    """

    def __init__(self, log_path: PathLike, loss_names: Sequence[str]):
        super().__init__(log_path)
        self.loss_names = loss_names

    def train(self, train_losses, step):
        values = np.mean(train_losses, axis=0)
        for name, value in zip_equal(self.loss_names, values):
            self.logger.log_scalar(f'train/loss/{name}', value, step)
