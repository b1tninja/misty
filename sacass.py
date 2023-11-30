from contextlib import closing

import requests


def get_parcel_details(apn):
    req = requests.get("https://assessorparcelviewer.saccounty.gov/GISWebService/api/gisapps/parcels/public/%d" % apn)
    assert req.status_code == 200
    return req.json()


def get_eproptax(apn):
    response = requests.get('https://eproptax.saccounty.net/servicev2/eproptax.svc/rest/BillSummary',
                            params=dict(parcel=apn))
    assert response.status_code == 200
    return response.json()


def download_taxbill(year_bill, dst):
    # 2 digit year + BillNumber
    params = {
        'BillNumber': year_bill,
        'billType': 'Secured',
        'assessType': 'Annual',
        'Installment': '2',
    }

    response = requests.get(
        'https://eproptax.saccounty.net/servicev2/eproptax.svc/rest/DownloadBillImage',
        params=params
    )

    assert response.headers['content-type'] == 'application/pdf'

    with closing(open(dst, 'wb')) as fh:
        fh.write(response.content)


def download_paymentstub(apn, report, dst):
    # report is YYYY + BilLNumber + 12

    response = requests.get(
        'https://eproptax.saccounty.net/servicev2/eproptax.svc/rest/GetReport/BillStub/%d' % apn,
        params=dict(ReportData=report),
    )

    assert response.headers['content-type'] == 'application/pdf'

    with closing(open(dst, 'wb')) as fh:
        fh.write(response.content)
