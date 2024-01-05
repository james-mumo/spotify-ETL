import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
import sqlite3


from dotenv import load_dotenv
import os
import base64
from requests import post


DATABASE_LOCATION = "sqlite:///spotify_etl.sqlite"
USER_ID = "eacc6ab82ad94c95afb9951ef2e88255"
USER_SECRET = "3e244642e788407186e8ee63849c8ba4"


def get_token(client_id, client_secret):
    auth_string = client_id + ";" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type":"client-credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    # token = json_result["access_token"]
    return json_result


s_token = get_token(client_id=USER_ID, client_secret=USER_SECRET)
print(s_token)

# TOKEN = get_spotify_api_token(client_id=client_id, client_secret=client_secret)



if __name__ == "__main__":
    headers = {
        "Accept":"application/json",
        "Content-Type":"applicattion/json",
        "Authorization":"Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) + 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()

    print(data)




