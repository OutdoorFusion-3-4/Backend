import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
from enum import Enum

class PredictableValues(Enum):
    Revenues = "revenues.pkl"
    Profits = "profits.pkl"

class Predictor: 
    def __init__(self):
        self.regressor = LinearRegression()

    def LoadData (self, dates: np.array, revenues:np.array):
        self.data_x = dates
        self.data_y = revenues
        return self

    def TrainModel(self, save: bool = True, 
                   saveTo: PredictableValues = PredictableValues.Revenues):
        self.regressor.fit(self.data_x, self.data_y)
        if save:
            joblib.dump(self.regressor, saveTo.value)
        return self
    
    def loadModel(self, loadFrom: PredictableValues = PredictableValues.Revenues):
        self.regressor = joblib.load(loadFrom.value)
        return self

    def Predict(self, futureDates: np.array, logs: bool = False):
        futureDates = np.array(futureDates).reshape(-1, 1)

        d = dict()
        d["prediction"] = self.regressor.predict(futureDates)

        if logs:
            d["coefficients"] = self.regressor.coef_
            d["intercept"] = self.regressor.intercept_
            return d 
        
        return d

