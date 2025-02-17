from fastapi import FastAPI
import uvicorn
import pandas as pd
from pycaret.classification import load_model

# Load the saved PyCaret model
model = load_model("best_model")

# Initialize FastAPI app
app = FastAPI()

# Define a request body schema
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class InputData(BaseModel):
    mileage_miles: int = Field(..., alias="Mileage(miles)")
    registration_year: int = Field(..., alias="Registration_Year")
    fuel_type: str = Field(..., alias="Fuel type")
    body_type: str = Field(..., alias="Body type")
    Engine: float
    Gearbox: str
    Doors: int
    Seats: int
    emission_class: str = Field(alias="Emission Class")

    class Config:
        allow_population_by_field_name = True
    
# Define prediction endpoint
@app.post("/predict")
def predict(data: InputData):
    
    df = pd.DataFrame([data.model_dump(by_alias=True)])
    # Make prediction
    prediction = model.predict(df)
    
    return {"prediction": prediction.tolist()[0]}



# Define request body schema for `/predStream`
class NewInputData(BaseModel):
    data: Dict[str, List]  # Expecting a dictionary where keys are column names

@app.post("/predStream/")
def predictFromStreamlit(payload: NewInputData):
    try:
        # Convert JSON back into a DataFrame
        df = pd.DataFrame.from_dict(payload.data)

        # Make prediction
        prediction = model.predict(df)

        return {"prediction": prediction.tolist()[0]}

    except Exception as e:
        return {"error": str(e)}


# Run the API locally
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
