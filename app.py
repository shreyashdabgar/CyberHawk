'''we are using here fast api'''

import os 
import sys
import certifi
import pymongo


from netwoksecurity.exception.exception import CustomException
from netwoksecurity.logging.logger import logging
from netwoksecurity.pipeline.training_pipeline import TrainingPipeline
from netwoksecurity.utills.main_utils.utils import *
from netwoksecurity.constents.traning_pipeline import * 
from netwoksecurity.entities.config_entity import *
from netwoksecurity.utills.ml_utills.model.estimetor import networkmodel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, requests
from fastapi.responses import Response
from uvicorn import run as app_run
from starlette.responses import RedirectResponse
import pandas as pd 
import numpy as np
from fastapi.templating import Jinja2Templates 


ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
db = client[DATA_INGESTION_DATABASE_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]

'''setup fast api'''
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

''' accesing templetes '''
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        logging.info("Training started")
        train_pipline = TrainingPipeline()
        train_pipline.run_pipeline()
        logging.info("Training completed")
        return Response("Training completed", status_code=200)
    
    except Exception as e:
        raise CustomException(e)
    



@app.post("/predict")
async def predict(request: requests.Request, file : UploadFile= File(...)):
    try:
        logging.info("prediiction is strated")
        df = pd.read_csv(file.file)
        preprocesser= load_obj("final_model\preprocesser.pkl")
        model= load_obj("final_model\model.pkl")
        network_model = networkmodel(preprocesser, model)
        prediction = network_model.predict(df)
        print(prediction)
        df['prediction'] = prediction
        df.to_csv('output/prediction.csv')
        table = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html", {"request" : request, "table" : table})

    except Exception as e :
        raise CustomException(e)

if __name__ == "__main__":
    app_run(app, host= "localhost", port = 8000)
