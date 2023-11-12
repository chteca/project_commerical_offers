import pandas as pd
import pickle

def preprocessing(data):
    #перевод даты в столбцы день, месяц, год и удаление колонки дата кп
    data['cp_date'] = pd.to_datetime(data['cp_date'])
    data['cp_day'] = data['cp_date'].dt.day
    data['cp_month'] = data['cp_date'].dt.month
    data['cp_year'] = data['cp_date'].dt.year
    data = data.drop('cp_date', axis=1)

    #encoding
    enc_model_file = './models/encoding_model.sav'
    enc_model = pickle.load(open(enc_model_file, 'rb'))
    data = enc_model.transform(data)

    return data