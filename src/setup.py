from dotenv import load_dotenv
import os
import json
import requests
import sys 
import platform

load_dotenv(".env")

TOKEN = os.getenv("TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
MONGO = os.getenv("MONGO")

LAVALINK_OPTIONS = {
    "uselavalink":False,
    "local":True
}

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

if LAVALINK_OPTIONS["uselavalink"] and LAVALINK_OPTIONS["local"]:
    if not os.path.exists(f"lavalink"):
        os.makedirs(f"lavalink")
    print("using Local Lavalink")
    if not os.path.isfile("lavalink/Lavalink.jar"):
        try:
            print('Downloading Lavalink.jar.')
            response = requests.get('https://github.com/lavalink-devs/Lavalink/releases/download/4.0.7/Lavalink.jar', stream=True)
            response.raise_for_status()
            with open("lavalink/Lavalink.jar", 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print('Lavalink success fully dowloaded')
        except requests.exceptions.RequestException as e:
            print(f'Fail to dowload Lavalike due to \n{e}')
            sys.exit()

    if not os.path.isfile(f"lavalink/application.yml"):
        try:
            print('Downloading application.yml.')
            response = requests.get('https://raw.githubusercontent.com/tunwit/Lavalink/main/application.yml', stream=True)
            response.raise_for_status()
            with open("lavalink/application.yml", 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print('application.yml success fully dowloaded')
        except requests.exceptions.RequestException as e:
            print(f'Fail to dowload application.yml due to \n{e}')
            sys.exit()

    start_check = False
    for filename in os.listdir("./"):
        if filename.startswith("start_lavalink"):
            start_check = True
    
    if not start_check:
        if platform.system() == "Windows":
            with open(f'start_lavalink.bat', "w") as bat_file:
                bat_file.write(f"""start cmd.exe /k "cd lavalink && java -jar lavalink.jar""")
        else:
            with open(f'start_lavalink.sh', "w") as bat_file:
                bat_file.write(f"""cd lavalink\njava -jar lavalink.jar""")
            print("Run this command \n'chmod +x ./start_lavalink.sh'")

config = {
    "TOKEN":TOKEN,
    "APPLICATION_ID":APPLICATION_ID,
    "MONGO":MONGO,
    "LAVALINK_OPTIONS":LAVALINK_OPTIONS
}
