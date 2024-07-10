from dotenv import load_dotenv
import os

load_dotenv(".env")

TOKEN = os.getenv("TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
MONGO = os.getenv("MONGO")

config = {
    "TOKEN":TOKEN,
    "APPLICATION_ID":APPLICATION_ID,
    "MONGO":MONGO
}

