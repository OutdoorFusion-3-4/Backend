import unittest
from core.ml import predictor
import numpy as np

class Test_Predictor(unittest.TestCase):
    def test_ml(self):
        # Example data
        dates = np.array([[1], [2], [3], [4], [5]]) 
        revenues = np.array([2, 4, 5, 4, 5])         
        expected = {
            "prediction":np.array([2.8, 3.4, 4.]), 
            "coefficients": np.array([0.6]), 
            "intercept": 2.2
        }
        print(expected)
        p = predictor.Predictor()
        p.LoadData(dates, revenues)
        p.TrainModel(False)

        results = p.PredictRevenue([1,2,3], True)
        if results["prediction"].all() == expected["prediction"].all() \
                and results["prediction"].all() == expected["prediction"].all() \
                and results["prediction"].all() == expected["prediction"].all():
            print("Test passed")
        

if __name__ == '__main__':
    unittest.main()