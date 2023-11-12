from pydantic import BaseModel, Field
from typing import List, Union
from datetime import date, datetime, timedelta


class PredictionInput(BaseModel):
    '''
    Pydantic model
    
    Example usage:
    input_data = PredictionInput(client='Client', procurement='Procurement info', delivery_time=60,
                                 catalog_number='1060072500, 1060352500', path_file='./image.png', quantity=10,
                                 contract=1, merck_competitors=1, other_competitors=1)
    '''

    client: str
    procurement: str
    delivery_time: int
    catalog_number: str | None = None
    path_file: str | None = None
    quantity: float
    contract: int
    merck_competitors: int
    other_competitors: int
    cp_date: datetime = Field(default_factory=datetime.now)


class PredictionOutput(BaseModel):
    '''
    Pydantic model
    
    Example usage:
    output = PredictionOutput(profitability=[30.02, 35.28])
    '''
    profitability: List[float]

