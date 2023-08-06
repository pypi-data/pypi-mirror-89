import copy
from abc import ABCMeta, abstractmethod


class BaseBaggingEnsemble(metaclass=ABCMeta):
    def __init__(self, estimator):
        self._estimator = estimator

    @abstractmethod
    def estimators_(self):  # pragma: no cover
        pass

    @abstractmethod
    def append(self):  # pragma: no cover
        pass

    def predict(self, X):
        return self._estimator.predict(X)

    def predict_proba(self, X):
        return self._estimator.predict_proba(X)

    def fit(self, X, y):
        self._estimator.fit(X, y)

    def __mult__(self, other):
        assert isinstance(other=float)

    def __add__(self, other):
        assert isinstance(other, BaseBaggingEnsemble)
        new = copy.deepcopy(self)
        new._estimators = new.append(other)
        return new