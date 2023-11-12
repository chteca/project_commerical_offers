from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field
from typing import List, Union
from preprocess import preprocessing
from datetime import datetime, timedelta
from utils import get_client_data, get_product_data
import pickle
import pandas as pd


class PredictionInput(BaseModel):
    client: str
    procurement: str
    delivery_time: int
    catalog_number: str
    quantity: float
    contract: int
    merck_competitors: int
    other_competitors: int
    cp_date: datetime

class PredictionOutput(BaseModel):
    profitability: List[float]

class RFModel:
    def __init__(self):
        self.model = None

    def load_model(self):
        model_file = './models/best_model_rfr.sav' 
        self.model = pickle.load(open(model_file, 'rb'))

    def predict_output(self, input: PredictionInput) -> PredictionOutput:
        if not self.model:
            raise RuntimeError("Model files are not found!")
        catalog_numbers = input.catalog_number.split(', ')
        data = pd.DataFrame({'client': input.client,
                               'industry': get_client_data(input.client, 'industry'),
                               'company_size': get_client_data(input.client, 'company_size'),
                               'private': get_client_data(input.client, 'private'),
                               'country': get_client_data(input.client, 'country'),
                               'town': get_client_data(input.client, 'town'),
                               'region': get_client_data(input.client, 'region'),
                               'procurement': input.procurement,
                               'delivery_time': input.delivery_time,
                               'terms_of_payment': get_client_data(input.client, 'terms_of_payment'),
                               'delivery_conditions': get_client_data(input.client, 'delivery_conditions'),
                               'direction': get_product_data(catalog_numbers, 'direction'),
                               'catalog_number': catalog_numbers,
                               'quantity': input.quantity,
                               'manufacturer': get_product_data(catalog_numbers, 'manufacturer'),
                               'product_category': get_product_data(catalog_numbers, 'product_category'),
                               'contract': input.contract,
                               'merck_competitors': input.merck_competitors,
                               'other_competitors': input.other_competitors,
                               'cp_date': input.cp_date
                               })
        
        data = preprocessing(data)

        output = self.model.predict(data)
        output = output.tolist()
        return output
