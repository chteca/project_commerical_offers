from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from schemas import PredictionInput, PredictionOutput, RFModel
import contextlib
import pickle
import tempfile
import shutil
from create_xls_file import create_xls_file


rf_model = RFModel() 

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    rf_model.load_model()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/prediction")
async def get_prediction(input: PredictionInput):
    output = rf_model.predict_output(input)

    workbook = create_xls_file(output, client=input.client, data=input.cp_date, catalog_number=input.catalog_number.split(', '), quantity=input.quantity)

    new_filename = "./cp/file1.xls"
    workbook.save(new_filename)

    return FileResponse(new_filename, media_type='application/vnd.ms-excel')