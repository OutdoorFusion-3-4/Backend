from enum import Enum
from flask import FileStorage
import pandas as pd
class FileTypes(Enum):
    Internal = "internal"
    External = "external"

class UploadFile():
    def __init__(self, file: FileStorage, fileType: FileTypes = FileTypes.Internal):
        self.file = file
        self.fileType = fileType
        return self
    # we should know the format of the file,
    # and also the shape of how the data is going to be stored in the database
    def parseCSV(self):
        dataframe = pd.read_csv(self.file)
        product = dataframe["Product"]
        quantity = dataframe["Quantity"]
        category = dataframe["Category"]
        
        if self.fileType == FileTypes.Internal:
            """Logic for internal file upload"""
        else :
            """Logic for external file upload"""


            
        

