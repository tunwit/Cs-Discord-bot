from dotenv import load_dotenv
import os
import json
load_dotenv(".env")

TOKEN = os.getenv("TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
MONGO = os.getenv("MONGO")

if not os.path.exists('database'):#if not exists Create one
    os.mkdir('database')

if not os.path.exists('database/data.json'): 
    data = {
    "manager": [],
    "role": {},
    "trackvc": {
        "channel": {}
    },
    "messagetrack": {
        "channel": {}
    },
    "joinleave": {
        "channel": {}
    },
    "absend_gen":{}
    }
    with open("database/data.json","w+") as f :
        data = json.dump(data,f,indent=4)

if not os.path.exists('database/signature'):
    os.mkdir('database/signature')


config = {
    "TOKEN":TOKEN,
    "APPLICATION_ID":APPLICATION_ID,
    "MONGO":MONGO
}

