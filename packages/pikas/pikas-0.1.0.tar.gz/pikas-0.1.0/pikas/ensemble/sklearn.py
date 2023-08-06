from pikas.ensemble.bagging import BaseBaggingEnsemble


class BaggingEnsemble(BaseBaggingEnsemble):
    @property
    def estimators_(self):
        return self._estimator.estimators_

    def append(self, other):
        self._estimator.estimators_.extend(other.estimators_)
        self._estimator.n_estimators = len(self.estimators_)
        return self
