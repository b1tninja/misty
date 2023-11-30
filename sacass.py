import requests


def get_parcel_details(apn):
    req = requests.get("https://assessorparcelviewer.saccounty.gov/GISWebService/api/gisapps/parcels/public/%d" % apn)
    assert req.status_code == 200
    return req.json()


def get_eproptax(apn):
    # headers = {
    #     'Accept': '*/*',
    #     'Accept-Language': 'en-US,en;q=0.9',
    #     'Cache-Control': 'no-cache',
    #     'Connection': 'keep-alive',
    #     'DNT': '1',
    #     'Origin': 'https://eproptax.saccounty.gov',
    #     'Pragma': 'no-cache',
    #     'Referer': 'https://eproptax.saccounty.gov/',
    #     'Sec-Fetch-Dest': 'empty',
    #     'Sec-Fetch-Mode': 'cors',
    #     'Sec-Fetch-Site': 'cross-site',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    #     'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"Windows"',
    # }

    response = requests.get(
        'https://eproptax.saccounty.net/servicev2/eproptax.svc/rest/BillSummary',
        params=dict(parcel=apn),
        # headers=headers,
    )
    assert response.status_code == 200

    return response.json()
