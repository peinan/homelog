import json
import traceback

import requests
from flask import Flask
from logzero import logger

from config import token
from spreadsheet import append_row, auth
from utils import timestamp


app = Flask(__name__)

@app.route('/logging/devices')
def loggin_devices():
    resp = json.loads(get_devices())
    ts = timestamp()
    date, time = ts.split(' ')
    values = [
        date, time,
        resp['temperature']['val'],
        resp['humidity']['val'],
        resp['illuminance']['val'],
        resp['motion']['val'],
    ]

    gs = None
    r = {}

    try:
        gs = auth()
    except:
        logger.error('auth failed: ' + traceback.format_exc())
    if gs:
        try:
            r = append_row(gs, values)
        except:
            logger.error(f'apeend failed: ' + traceback.format_exc())

    return json.dumps(r)


@app.route('/devices')
def get_devices():
    url = 'https://api.nature.global/1/devices'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        resp = dict(
            status='ERROR',
            message=f'failed: {r.status_code}'
        )
    else:
        rjson = r.json()[0]
        humidity    = rjson['newest_events']['hu']
        illuminance = rjson['newest_events']['il']
        motion      = rjson['newest_events']['mo']
        temperature = rjson['newest_events']['te']

        resp = dict(
            status='SUCCESS',
            message='',
            humidity=humidity,
            illuminance=illuminance,
            motion=motion,
            temperature=temperature,
        )

    return json.dumps(resp, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
