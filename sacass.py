import tqdm
# Address.csv
# https://prod-hub-indexer.s3.amazonaws.com/files/54b1835ffb7b4e728a3506fe1a23618d/1/full/2226/54b1835ffb7b4e728a3506fe1a23618d_1_full_2226.csv

import csv
import json
import logging
import os
import random
from asyncio import Semaphore

import aiohttp

BASE_DIR = 'sacass'
c = 25

import asyncio
from aiohttp import ContentTypeError


async def apn_json(session: aiohttp.ClientSession, apn: str):
    url = 'https://assessorparcelviewer.saccounty.net/GISWebService/GISWebservice.svc/parcels/public/%s' % apn
    json_path = os.path.join(BASE_DIR, '%s.json' % apn)
    if os.path.exists(json_path):
        with open(json_path, 'r') as fh:
            try:
                o = json.load(fh)
                return apn, o
            except json.JSONDecodeError:
                pass

    async with session.get(url) as response:
        assert response.status == 200
        try:
            o = dict(await response.json())
        except ContentTypeError:
            logging.warning("ContentTypeError for %s" % url)
        else:
            with open(json_path, 'w') as fh:
                json.dump(o, fh)
            return apn, o


async def download_apns(session: aiohttp.ClientSession, apns: list):
    download_futures = [apn_json(session, apn) for apn in apns]
    for download_future in asyncio.as_completed(download_futures):
        try:
            ret = await download_future
        except ContentTypeError:
            pass
        except json.JSONDecodeError:
            pass
        else:
            if ret is not None:
                apn, data = ret
                # print(apn, data.get('FullAddress'))

    return True


async def main():
    with open('Address.csv', 'r') as fh:
        dr = csv.DictReader(fh)
        apns = [r['Parcel_Number'] for r in dr]

    random.shuffle(apns)
    async with aiohttp.ClientSession() as session:
        for n in tqdm.tqdm(range(0, len(apns), c)):
            await download_apns(session, apns[n:][:c])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
