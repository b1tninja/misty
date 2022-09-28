import os
from datetime import date

import requests


def login(email, password):
    headers = {
        'authority': 'sacramento.agencycounter.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'agency-counter-tenant': 'sacramento',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://sacramento.agencycounter.com',
        'pragma': 'no-cache',
        'referer': 'https://sacramento.agencycounter.com/?login',
    }

    response = requests.post('https://sacramento.agencycounter.com/api/auth/login', headers=headers,
                             json=dict(email=email, password=password))

    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 200
    assert body['data']['token_type'] == 'bearer'
    return body['data']['access_token']


def location(token, address=None):
    headers = {
        'authority': 'sacramento.agencycounter.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'agency-counter-module': 'home',
        'agency-counter-tenant': 'sacramento',
        'authorization': 'Bearer ' + token,
        # 'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://sacramento.agencycounter.com',
        'pragma': 'no-cache',
        'referer': 'https://sacramento.agencycounter.com/?tab=map',
    }

    json_data = {
        '___viewport': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [
                                    -121.56012,
                                    38.685506,
                                ],
                                [
                                    -121.36274,
                                    38.685506,
                                ],
                                [
                                    -121.36274,
                                    38.437574,
                                ],
                                [
                                    -121.56012,
                                    38.437574,
                                ],
                                [
                                    -121.56012,
                                    38.685506,
                                ],
                            ],
                        ],
                    },
                    'properties': {},
                },
            ],
        },
        '___address': address or '',
        'agency_reference': '',
        'name': '',
        'record_date___start': '2010-01-01',
        'record_date___end': date.today().strftime('%Y-%m-%d'),
        'status_category_id_internal': [
            1,
            2,
        ],
        'record_type': 'all',
    }

    response = requests.post('https://sacramento.agencycounter.com/api/search/location', headers=headers,
                             json=json_data)
    assert response.status_code == 200
    json = response.json()
    return json['data']


def detail(token, guids):
    headers = {
        'authority': 'sacramento.agencycounter.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'agency-counter-module': 'home',
        'agency-counter-tenant': 'sacramento',
        'authorization': 'Bearer ' + token,
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://sacramento.agencycounter.com',
        'pragma': 'no-cache',
        'referer': 'https://sacramento.agencycounter.com/?tab=map',
    }

    json_data = {
        '___viewport': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [
                                    -121.56012,
                                    38.685506,
                                ],
                                [
                                    -121.36274,
                                    38.685506,
                                ],
                                [
                                    -121.36274,
                                    38.437574,
                                ],
                                [
                                    -121.56012,
                                    38.437574,
                                ],
                                [
                                    -121.56012,
                                    38.685506,
                                ],
                            ],
                        ],
                    },
                    'properties': {},
                },
            ],
        },
        '___address': '',
        'agency_reference': '',
        'name': '',
        'record_date___start': '2010-01-01',
        'record_date___end': date.today().strftime('%Y-%m-%d'),
        'status_category_id_internal': [
            1,
            2,
        ],
        'record_type': 'all',
        '___location': guids,
    }

    response = requests.post('https://sacramento.agencycounter.com/api/search/detail', headers=headers,
                             json=json_data)
    return response.json()


if __name__ == '__main__':
    token = login(os.environ['AGENCYCOUNTER_USERNAME'], os.environ['AGENCYCOUNTER_PASSWORD'])
    data = location(token, address='3000 MACON DR')

    import pprint

    pprint.pprint(data)
    guids = [feature['properties']['guid'] for feature in data['features']]

    details = detail(token, guids)
    pprint.pprint(details)
