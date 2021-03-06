import asyncio
import csv
import json
import logging
import os
import random
import sys

import aiohttp
import tqdm
from aiohttp import ContentTypeError

# TODO: lulz
# from misty.utils import print_and_say as print

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def download(session: aiohttp.ClientSession, url, path):
    """
    Downlaod url to path
    """

    logger.info("Download %s to %s", url, path)
    async with session.get(url) as response:
        assert response.status == 200
        content = await response.read()

        if content:
            with open(path, mode='wb') as fh:
                fh.write(content)

            return content


async def apn_json(session: aiohttp.ClientSession, apn: str):
    # TODO: Consider replacing with download
    url = 'https://assessorparcelviewer.saccounty.net/GISWebService/GISWebservice.svc/parcels/public/%s' % apn
    async with session.get(url) as response:
        assert response.status == 200
        try:
            o = dict(await response.json())
        except ContentTypeError:
            logging.warning("\nContentTypeError for %s" % url)
        else:
            return apn, o


async def download_apns(session: aiohttp.ClientSession,
                        apns: list,
                        json_dir: str):
    """
    Download the apns list of APN jsons into json_dir
    """

    download_futures = [apn_json(session, apn) for apn in apns]
    for download_future in asyncio.as_completed(download_futures):
        try:
            ret = await download_future
        except ContentTypeError:
            pass
        except json.JSONDecodeError:
            logger.debug("Received invalid JSON")

        if ret is None:
            continue

        apn, data = ret

        try:
            assert data['APN'] == apn
        except AssertionError:
            logging.warning("\nServer returned wrong JSON, asked for %s got %s", apn, data['APN'])
            continue

        logging.debug("APN: %s, FullAddress: %s", apn, data.get('FullAddress'))

        json_path = os.path.join(json_dir, apn + '.json')
        with open(json_path, 'w') as fh:
            json.dump(data, fh)


async def suggestions(session, query):
    # TODO: lol urljoin and urlencode
    url = 'https://assessorparcelviewer.saccounty.net/GISWebService/Autocomplete.svc/suggest?prefixText=%s&count=15&filter=Assessor' % query
    async with session.get(url) as response:
        assert response.status == 200
        return await response.json()



async def main(root_dir,
               download=True,
               connections=100,
               per_host=10,
               validate_jsons=True,
               unlink=False):
    """
    Sacramento Assessor Parcel JSON downloader
    """
    data_dir = os.path.join(root_dir, 'sacass')
    os.makedirs(data_dir, exist_ok=True)

    address_csv = os.path.join(data_dir, 'Address.csv')
    downloads = {
        address_csv:
            'https://prod-hub-indexer.s3.amazonaws.com/files/54b1835ffb7b4e728a3506fe1a23618d/1/full/2226/54b1835ffb7b4e728a3506fe1a23618d_1_full_2226.csv',
    }

    # Download needed files
    async with aiohttp.ClientSession(connector=aiohttp.connector.TCPConnector(limit=connections,
                                                                              limit_per_host=per_host)) as session:
        for name, url in downloads.items():
            path = os.path.join(data_dir, name)
            if not os.path.exists(path):
                await download(session, url, path)

    json_dir = os.path.join(data_dir, 'jsons')
    os.makedirs(json_dir, exist_ok=True)

    # TODO: pool.map_async(validate_json, jsons, error_callback=)
    # TODO: def verify_jsons():
    jsons = [p for p in os.listdir(json_dir) if p.endswith('.json')]
    logging.info("Found %d json files.", len(jsons))

    bad_jsons = []
    if validate_jsons:
        logging.info("Validating json files...")
        # Cleanup any partially written or invalid JSONs
        for name in tqdm.tqdm(os.listdir(json_dir)):
            path = os.path.join(json_dir, name)
            if not path.endswith('.json'):
                continue

            try:
                with open(path, mode="r") as fh:
                    data = json.load(fh)
                    assert data['APN'] == name[:-5]
            except (json.JSONDecodeError, AssertionError) as e:
                logger.debug("%s: %s", path, e)
                bad_jsons.append(path)


        logger.info("Checked %d jsons, removing %d invalid jsons.", len(jsons), len(bad_jsons))

    if unlink:
        for bad_json in bad_jsons:
            assert bad_json.endswith('.json')
            os.unlink(bad_json)

    existing_jsons = set(jsons) - set(bad_jsons)

    # Get list of APNs
    with open(address_csv, 'r') as fh:
        dr = csv.DictReader(fh)
        apns = list({r['Parcel_Number'] for r in dr} - {p[:-5] for p in existing_jsons})

    random.shuffle(apns)

    async with aiohttp.ClientSession(connector=aiohttp.connector.TCPConnector(limit_per_host=per_host)) as session:
        if download:
            logging.info("Downloading %d APNs", len(apns))
            for n in tqdm.tqdm(range(0, len(apns), connections)):
                await download_apns(session, apns[n:][:connections], json_dir)

        # Find intersecting streets of WHIMSICAL
        for suggestion in await suggestions(session, 'WHIMSICAL'):
            print(suggestion)



def dir_path(path):
    logger.info("Checking --path: %s", path)

    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Sacramento County Assessors Parcel JSON downloader.')
    parser.add_argument('--path', type=dir_path, default='data', help="Data directory")

    parser.add_argument('-c', '--connections', type=int, default=100, help="Connection Limit")
    parser.add_argument('-l', '--limit-per-host', type=int, default=10, help="limit per host")

    try:
        parser.add_argument('-d', '--download', action=argparse.BooleanOptionalAction, default=True)
        parser.add_argument('-v', '--verify', action=argparse.BooleanOptionalAction, default=False)
        parser.add_argument('-u', '--unlink', action=argparse.BooleanOptionalAction, default=False, help="Remove invalid JSONs")
    except:
        parser.add_argument('-d', '--download', action="store_true")
        parser.add_argument('-v', '--verify', action="store_true")
        parser.add_argument('-u', '--unlink', action="store_true")

    try:
        args = parser.parse_args()

        if args.unlink:
            # implicit verify
            args.verify = True

    except NotADirectoryError:
        logger.critical("Please specify a path to a directory to download data into.")
        parser.print_help(sys.stderr)
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(args.path,
                                     download=args.download,
                                     connections=args.connections,
                                     per_host=args.limit_per_host,
                                     validate_jsons=args.verify,
                                     unlink=args.unlink,
                                     ))
