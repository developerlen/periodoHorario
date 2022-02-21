import requests
from telecontagem.secret import USER, PASSWORD
import json
import pandas as pd
import os
import sys
from common.utils import write_excel

BASE_URL = "https://api.privado.observatorios-lisboa.pt"
dir_path = os.path.dirname(os.path.realpath(__file__))

session = requests.Session()


def get_token():  # get api access token
    response = requests.post(
        f"{BASE_URL}/auth/login/", data={"username": USER, "password": PASSWORD}
    )
    tokens = json.loads(response.content)
    return tokens["access"]


def refresh_token(r, *args, **kwargs):  # refresh api access token
    if r.status_code == 401:
        print("Fetching new token as the previous token expired")
        token = get_token()
        session.headers.update({"Authorization": f"Bearer {token}"})
        r.request.headers["Authorization"] = session.headers["Authorization"]
        return session.send(r.request, verify=False)


session.headers.update({"Authorization": f"Bearer {get_token()}"})
session.hooks["response"].append(refresh_token)


def get_telecontagem(cpe: str, date_start: str, date_end: str):
    print(f"\ngetting telecontagem for {cpe} between {date_start} and {date_end}")
    url = (
        f"{BASE_URL}/energy/telemetering/?cpes={cpe}&start={date_start}&end={date_end}"
    )

    with session.get(url) as res:
        if res.status_code >= 400:
            raise ValueError(json.loads(res.content))
        df = pd.DataFrame(json.loads(res.content))

    filename = f"{cpe}_{date_start}_{date_end}.xlsx"
    write_excel(df, dir_path, filename)


if __name__ == "__main__":
    args = list(sys.argv)
    cpes = args[1:-2]
    date_start = args[-2]
    date_end = args[-1]

    if not cpes:  # if no cpes are passed in the comand, read them from the .txt file
        with open("cpes.txt", "r") as cpes_file:
            cpes = [c.strip() for c in cpes_file]

    cpes = list(set(cpes))
    for cpe in cpes:
        get_telecontagem(cpe, date_start, date_end)
