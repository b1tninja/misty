import csv
import json
import logging
import os
from operator import itemgetter

import requests
from tqdm import tqdm


from misty.utils import print_and_say as print

def get_suggestions(query):
    # TODO: lol urlunparse and urlencode
    url = 'https://assessorparcelviewer.saccounty.net/GISWebService/Autocomplete.svc/suggest?prefixText=%s&count=15&filter=Assessor' % query
    # TODO: i got 99 problems and a cert aint none
    response = requests.get(url, verify=False)
    assert response.status_code == 200
    return response.json()


def lod2csv(path, rows,
            group_by=None,
            ignore=None,
            sort_by=None,
            reprs=None):
    """list of dictionaries to CSV"""
    if ignore is None:
        ignore = list()

    if reprs is None:
        reprs = dict()

    keys = rows[0].keys()  # TODO: set([r.keys() for r in l]), bonus points for next()/iter

    # TODO: consider frozenset(o.items()) as __hash__

    ud = dict([(int(o[group_by]), o) for o in rows]) if group_by else enumerate(rows)
    with open(path, 'w', newline='') as fh:
        dw = csv.DictWriter(fh, [k for k in keys if k not in ignore], delimiter='\t')
        dw.writeheader()
        dw.writerows([dict(((k, reprs.get(k, lambda v: v)(v)) for k, v in r.items() if k not in ignore)) for r in
                      (sorted(ud.values(), key=itemgetter(sort_by)) if sort_by else rows)])


if __name__ == '__main__':
    root_dir = os.path.join(r"D:\misty", 'sacass')
    os.makedirs(root_dir, exist_ok=True)

    jsons = []
    json_dir = os.path.join(root_dir, 'jsons')
    for name in tqdm(os.listdir(json_dir)):
        if not name.endswith('.json'):
            continue

        path = os.path.join(json_dir, name)

        if not os.path.isfile(path):
            continue

        logging.debug(name)

        try:
            with open(path, 'r') as fh:
                data = json.load(fh)

        except json.JSONDecodeError as e:
            logging.error(e)
            continue

        else:
            jsons.append(data)

    # datetime.datetime.fromtimestamp
    # strptime /Date(timstamp000%z)/
    # v.split('-')
    # int(v[6:][:-2])

    filters = {
        'MESMERIZING WALK',
        # 'PICASSO CIR',
        # 'KANDINSKY WAY',
        # 'UNNAMED RD',
        'ENCHANTED WALK',
        # 'MACON DR',
        'WHIMSICAL LN',
        'MAGICAL WALK',
    }
    if not filters:
        # Use County Assessors suggestions API to Find intersecting street names.
        query = "WHIMSICAL"
        suggestions = [suggestion.split(' at ') for suggestion in get_suggestions(query)]
        streets = {a for b in suggestions for a in b}
        for street in streets:
            print(street)

        filters = streets

    filter_by = 'FullAddress'

    rows = sorted([o for o in jsons if not filters or any(v in o[filter_by] for v in filters)],
                  key=itemgetter('DocumentDate'), reverse=True)

    if not rows:
        logging.warning("No rows!")

    for value in set(map(itemgetter('FullAddress'), rows)):
        print(value)

    csv_name = 'rows.csv'
    csv_path = os.path.join(root_dir, csv_name)

    lod2csv(csv_path, rows,
            group_by='APN',
            sort_by='DocumentDate',
            ignore=[
                'APN',
                # 'APN_DASH',
                'AddressOfInterest',
                'Addresses',
                # 'Bathrooms',
                # 'Bedrooms',
                'Block',
                'CareOf',
                'Centroid',
                'City',
                # 'DocumentDate',
                # 'DocumentPage',
                # 'DocumentType',
                'DocumentTypeDescription',
                'EventDate',
                'EventPage',
                # 'FullAddress',
                'GISPCNStatusCreated',
                'GISPCNStatusObsoleted',
                'GISParcelType',
                'GISType',
                'Geometry',
                'Jurisdiction',
                'LandUseCode',
                'Landmark',
                'LastRollYear',
                'LongLegalDescription',
                'Lot',
                # 'LotSize',
                'MailAddress1',
                'MailAddress2',
                'NeighborhoodCode',
                'Owner',
                'OwnerStatus',
                'PCNCreatedBy',
                'PCNCreatedDate',
                'PCNDeletedBy',
                'PCNObsoleteDate',
                'ParcelStatus',
                'SitusAddress1',
                'SitusAddress2',
                'SitusZip',
                'Stories',
                'SubdivisionCode',
                'SubdivisionName',
                'TaxJurisdiction',
                'TaxRateAreaCode',
                'TotalLivingArea',
                # 'Unit'
            ])
