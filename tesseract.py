import pytesseract
from PIL import Image
import pandas as pd

def get_catalog_numbers(file_path, product_data = pd.read_csv('./data/prices.csv')):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    text = text.replace(' ', '').replace('O', '0').replace("I", '1')
    supposed_cat_num = [text[i:i+9] for i in range(len(text)-9)] + [text[i:i+10] for i in range(len(text)-10)]
    catalog_numbers = [c for c in cat if c in list(product_data.catalog_number.values)]
    return catalog_numbers