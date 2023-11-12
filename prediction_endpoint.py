from fastapi import FastAPI, UploadFile, HTTPException, status, Depends
from fastapi.responses import FileResponse
from schemas import PredictionInput, PredictionOutput
import contextlib
import pickle
import tempfile
import shutil
from create_xls_file import create_xls_file
from tesseract import get_catalog_numbers
from utils import RFModel

rf_model = RFModel() 

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    rf_model.load_model()
    #await create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/prediction", response_model=PredictionOutput)
async def get_prediction(input: PredictionInput):
    output = rf_model.predict_output(input)

    if input.catalog_number:
            catalog_numbers = input.catalog_number.split(', ')
    elif input.path_file:
        catalog_numbers = get_catalog_numbers(input.path_file)

    workbook = create_xls_file(output, client=input.client, data=input.cp_date, catalog_number=catalog_numbers, quantity=input.quantity)

    output = PredictionOutput(profitability=output)

    new_filename = "./cp/file1.xls"
    workbook.save(new_filename)

    return output



