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
    data: Dict[str, List]

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
    
@app.post("/predBatch/")
def batchPredict(payload: NewInputData):
    try:
        # Convert JSON back into a DataFrame
        df = pd.DataFrame.from_dict(payload.data)

        # Make prediction
        prediction = model.predict(df)

        return {"prediction": prediction.tolist()}

    except Exception as e:
        return {"error": str(e)}
    

# Run the API locally
if __name__ == "__main__":
    # import requests
    # import pandas as pd
    # url = "http://127.0.0.1:8000/predBatch/"
    # df = pd.read_csv(r"data\Cleaned_used_cars_data.csv")
    # df = df.head()
    # df.drop('Price', axis=1, inplace=True)
    # json_data = {"data": df.to_dict(orient="list")}
    # print(json_data)
    # response = requests.post(url, json=json_data)
    # print(response.json())
    uvicorn.run(app, host="127.0.0.1", port=8000)
