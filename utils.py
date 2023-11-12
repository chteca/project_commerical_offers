import pandas as pd

client_data = pd.read_csv('./data/clients.csv')
product_data = pd.read_csv('./data/prices.csv')

def get_client_data(client_name, search_column):
    return client_data.loc[client_data.client == client_name, search_column].values[0]

def get_product_data(cat_numbers, search_column):
    return [product_data[product_data.catalog_number == cat_num][search_column].iloc[0] for cat_num in cat_numbers]

def get_product_info(cat_numbers, search_column):
    return product_data[product_data.catalog_number == cat_numbers][search_column].iloc[0]



