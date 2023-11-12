import pandas as pd
from datetime import date, datetime, timedelta
import pickle
import pandas as pd
from tesseract import get_catalog_numbers
from preprocess import preprocessing
from schemas import PredictionInput, PredictionOutput

product_data = pd.read_csv('./data/prices.csv')

def get_client_data(client_name, search_column, client_data=pd.read_csv('./data/clients.csv')):
    '''
    Retrieves data for a specific client from client_data based on the given client_name and search_column
    
    Args:
    client_name: str - a name of the client.
    search_column: str -a name of the column in client_data to search for the client_name.
    client_data: pd.DataFrame - a dataframe with information about clients

    Returns the value of the specified search_column for the given client_name.

    Example usage:
    full_name = get_client_data('Client', 'full_name')
    '''

    return client_data.loc[client_data.client == client_name, search_column].values[0]


def get_product_data(cat_numbers, search_column, product_data = pd.read_csv('./data/prices.csv')):
    '''
    Retrieves data from a CSV file containing product information based on the provided catalog numbers and search column
    
    Args:
    cat_numbers: list[str] - a list of catalog numbers for which data needs to be retrieved
    search_column: str - a specific column to search within the product data
    product_data: pd.DataFrame - a dataframe with information about products

    Returns  list of values obtained from the specified search column in the product data for each catalog number supplied

    Example usage:
    directions = get_product_data(['1060072500', '1060352500'], 'direction')
    '''
    return [product_data[product_data.catalog_number == cat_num][search_column].iloc[0] for cat_num in cat_numbers]


def get_product_info(cat_numbers, search_column, product_data = pd.read_csv('./data/prices.csv')):
    '''
    Retrieves information about a product based on it's catalog number

    Args:
    cat_numbers: str - a catalog number for which information is to be retrieved
    search_column: str -  a column in the product data to search for the information.
    product_data: pd.DataFrame - a product data containing the information

    Returns value in the specified `search_column` for the product with the given `cat_numbers`.

    Example usage:
    directions = get_product_data('1060072500', 'direction')
    '''
    return product_data[product_data.catalog_number == cat_numbers][search_column].iloc[0]



class RFModel:
    """
    A class representing a Random Forest Model for prediction.

    Methods:
    - __init__(): Initializes the RFModel class.
    - load_model(): Loads the trained model from a file.
    - predict_output(input: PredictionInput) -> PredictionOutput: Predicts the output based on input data.

    Attributes:
    - model: The trained Random Forest model.
    """

    def __init__(self):
        self.model = None

    def load_model(self):
        """
        Loads the trained Random Forest model from a file.
        """

        model_file = './models/best_model_rfr.sav' 
        self.model = pickle.load(open(model_file, 'rb'))

    def predict_output(self, input: PredictionInput) -> PredictionOutput:
        """
        Predicts the output based on the given input data

        Args:
        input: PredictionInput -  The input data for prediction

        Returns output (PredictionOutput): The predicted output based on the input data
        """
        
        if not self.model:
            raise RuntimeError("Model files are not found!")
        catalog_numbers = []
        if input.catalog_number:
            catalog_numbers = input.catalog_number.split(', ')
        elif input.path_file:
            catalog_numbers = get_catalog_numbers(input.path_file)
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



