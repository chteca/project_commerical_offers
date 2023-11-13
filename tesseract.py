import pytesseract
from PIL import Image
import pandas as pd

def get_catalog_numbers(file_path, product_data=pd.read_csv('./data/prices.csv')):
    '''
    Retrieves catalog numbers from an image file using Tesseract OCR 

    Args:
    file_path: str - path to the image file
    product_data: pd.DataFrame - DataFrame containing product data with a column 'catalog_number'

    Returns a list of catalog numbers detected in the image and present in the provided product data.

    Example usage:
    catalog_numbers = get_catalog_numbers('image.jpg')
    '''
    
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    text = text.replace(' ', '').replace('O', '0').replace('-', '').replace('!', '1')
    supposed_cat_num = [text[i:i+9] for i in range(len(text)-9)] + [text[i:i+10] for i in range(len(text)-10)]
    catalog_numbers = [c for c in supposed_cat_num if c in list(product_data.catalog_number.values)]
    text = text.replace('I', '1')
    changed_text_cn = [text[i:i+9] for i in range(len(text)-9)] + [text[i:i+10] for i in range(len(text)-10)]
    changed_cn = [c for c in changed_text_cn if c in list(product_data.catalog_number.values) and c not in catalog_numbers]
    catalog_numbers.extend(changed_cn)

    return catalog_numbers