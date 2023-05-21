import unittest
from core.ml import predictor

import numpy as np
import os


class Test_Predictor(unittest.TestCase):
    dates = np.array([[1], [2], [3], [4], [5]])
    revenues = np.array([2, 4, 5, 4, 5])
    expected = {
        "prediction": np.array([2.8, 3.4, 4.]),
        "coefficients": np.array([0.6]),
        "intercept": 2.2
    }

    def test_loadDataAndTrain(self):
        p = predictor.Predictor()
        results = p.LoadData(self.dates, self.revenues)\
            .TrainModel(False)\
            .Predict([1, 2, 3], True)

        if results["prediction"].all() == self.expected["prediction"].all() \
                and results["prediction"].all() == self.expected["prediction"].all() \
                and results["prediction"].all() == self.expected["prediction"].all():
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_saveDataReloadAndPredict(self):
        p = predictor.Predictor()
        p.LoadData(self.dates, self.revenues)\
            .TrainModel(True)

        q = predictor.Predictor()
        results = q.loadModel()\
            .Predict([1, 2, 3], True)

        # Delete the saved model after prediction test
        os.remove(predictor.PredictableValues.Revenues.value)

        if results["prediction"].all() == self.expected["prediction"].all() \
                and results["prediction"].all() == self.expected["prediction"].all() \
                and results["prediction"].all() == self.expected["prediction"].all():

            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
