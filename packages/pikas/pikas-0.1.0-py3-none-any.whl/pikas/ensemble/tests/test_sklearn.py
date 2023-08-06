from pikas.ensemble.sklearn import BaggingEnsemble
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np


class TestBaggingEnsemble:
    def setup_method(self):
        self.X, y = load_diabetes(return_X_y=True)

        self.est = RandomForestRegressor(n_estimators=5, n_jobs=-1, random_state=42)
        self.est.fit(self.X, y)

        self.est2 = RandomForestRegressor(n_estimators=5, n_jobs=-1, random_state=43)
        self.est2.fit(self.X, y)

        self.ensemble = BaggingEnsemble(self.est)

    def test_estimators_(self):
        assert self.ensemble.estimators_ == self.est.estimators_

    def test_predict(self):
        assert np.allclose(self.ensemble.predict(self.X), self.est.predict(self.X))

    def test__add__(self):
        new = BaggingEnsemble(self.est) + BaggingEnsemble(self.est2)

        assert len(new.estimators_) == self.est.n_estimators + self.est2.n_estimators
        new_pred = new.predict(self.X)
        manual_ensemble = 0.5 * (self.est.predict(self.X) + self.est2.predict(self.X))

        assert np.allclose(new_pred, manual_ensemble)
