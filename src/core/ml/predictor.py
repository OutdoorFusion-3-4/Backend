import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

class Predictor: 
    def __init__(self):
        self.regressor = LinearRegression()

    def LoadData (self, dates: np.array, revenues:np.array):
        self.data_x = dates
        self.data_y = revenues

    def TrainModel(self, save: bool = True):
        self.regressor.fit(self.data_x, self.data_y)
        if save:
            joblib.dump(self.regressor, "model.pkl")
    
    def loadModel(self):
        self.regressor = joblib.load("model.pkl")

    def PredictRevenue(self, futureDates: np.array, logs: bool = False):
        futureDates = np.array(futureDates).reshape(-1, 1)

        d = dict()
        d["prediction"] = self.regressor.predict(futureDates)

        if logs:
            d["coefficients"] = self.regressor.coef_
            d["intercept"] = self.regressor.intercept_
            return d 
        
        return d
