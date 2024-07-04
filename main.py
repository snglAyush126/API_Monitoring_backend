import string
from typing import Union

from datetime import date 

from fastapi import FastAPI, Response

from fastapi.middleware.cors import CORSMiddleware


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/usage/{month}/{year}")
async def read_item(month: int, year:int, userToken: str | None = None):

    myclient = pymongo.MongoClient("mongodb+srv://snglayush:Ayush123@cluster0.p5tsrwd.mongodb.net/API_MONITORING")
    mydb = myclient["mydatabase"]
    mydownloadcol = mydb["downloads"]
    mychatcol = mydb["chats"]

    downloadDatas = []
    chatDatas = []

    for downloadData in mydownloadcol.find({"month" : month, "year" : year, "userToken" : userToken}):
        print(downloadData)
        downloadDatas.append({"day":downloadData["day"],"month":downloadData["month"], "year":downloadData["year"], "data_id":downloadData["data_id"]})
    for chatData in mychatcol.find({"month" : month, "year" : year, "userToken" : userToken}):
        print(chatData)
        chatDatas.append({"day":chatData["day"],"month" : chatData["month"], "year" : chatData["year"], "chat_id" : chatData["chat_id"]})
    
    return {"downloadDatas" : downloadDatas, "chatDatas" : chatDatas}


@app.get("/download/{data_id}")
async def read_item(data_id: str, userToken: str | None = None):

  
    todays_date = date.today() 


    myclient = pymongo.MongoClient("mongodb+srv://snglayush:Ayush123@cluster0.p5tsrwd.mongodb.net/API_MONITORING")
    mydb = myclient["mydatabase"]
    mycol = mydb["downloads"]

    mydict = {"year":todays_date.year, "month":todays_date.month, "day":todays_date.day,"data_id":data_id, "userToken":userToken}

    x = mycol.insert_one(mydict)
    
    return {"userToken":userToken}

@app.get("/chat/{chat_id}")
async def read_item(chat_id: int, userToken: str | None = None):

    myclient = pymongo.MongoClient("mongodb+srv://snglayush:Ayush123@cluster0.p5tsrwd.mongodb.net/API_MONITORING")
    mydb = myclient["mydatabase"]
    mycol = mydb["chats"]

    todays_date = date.today() 

    mydict = {"year":todays_date.year, "month":todays_date.month, "day":todays_date.day,"chat_id": chat_id, "userToken":userToken}

    x = mycol.insert_one(mydict)

    return {"userToken":userToken}