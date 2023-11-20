import csv

import requests

from sacrec import clerk_search, clerk_get_names_for_document_id

apns = [20111700220010, 20111700220011, 20111700220012, 20111700220013, 20111700220014, 20111700220015, 20111700220016,
        20111700230023, 20111700230022, 20111700230021, 20111700230020, 20111700230019, 20111700230018, 20111700230017,
        20111700230016, 20111700230015, 20111700230014, 20111700240001, 20111700240002, 20111700240003, 20111700240004,
        20111700240005, 20111700240006, 20111700240007, 20111700240008, 20111700240009, 20111700240010, 20111700240011,
        20111700240012, 20111700250023, 20111700250022, 20111700250021, 20111700250020, 20111700250019, 20111700250018,
        20111700250017, 20111700250016, 20111700250015, 20111700250014, 20111700260014, 20111700260015, 20111700260016,
        20111700260017, 20111700260018, 20111700260019, 20111700260020, 20111700260021, 20111700260022, 20111700260023,
        20111700270023, 20111700270022, 20111700270021, 20111700270020, 20111700270019, 20111700270018, 20111700270017,
        20111700270016, 20111700270015, 20111700270014, 20111700280014, 20111700280015, 20111700280016, 20111700280017,
        20111700280018, 20111700280019, 20111700280020, 20111700280021, 20111700280022, 20111700280023, 20111700170001,
        20111700170002, 20111700170003, 20111700170004, 20111700170005, 20111700170006, 20111700170007, 20111700170008,
        20111700170009, 20111700170010, 20111700170011, 20111700170012]

with open('members.csv', 'w', newline='') as fh:
    writer = csv.writer(fh, dialect=csv.excel_tab)

    for apn in apns:
        req = requests.get(
            "https://assessorparcelviewer.saccounty.gov/GISWebService/api/gisapps/parcels/public/%d" % apn)
        assert req.status_code == 200
        parcel = req.json()
        document_number = parcel['DocumentBook'] + parcel['DocumentPage'].zfill(4)
        docs = clerk_search(SearchText=document_number,
                            IsBasicSearch='true',
                            IsExactMatch='true')
        assert len(docs['SearchResults']) == 1
        doc = docs['SearchResults'][0]
        assert doc['PrimaryDocNumber'] == document_number
        # names = doc['Names'].split('<br/>')
        # grantees = [name[4:] for name in names if name.startswith('(E) ')]
        # grantors = [name[4:] for name in names if name.startswith('(R) ')]
        names = clerk_get_names_for_document_id(doc['ID'])
        grantors = [entity['Fullname'] for entity in names if entity['NameTypeDesc'] == 'Grantor']
        grantees = [entity['Fullname'] for entity in names if entity['NameTypeDesc'] == 'Grantee']

        parcel_keys = [
            'APN',
            'Bathrooms',
            'Bedrooms',
            'DocumentBook',
            'DocumentPage',
            'DocumentType',
            'FullAddress',
            'Stories',
            'TotalLivingArea',
            'Unit'
        ]
        row = (*tuple([parcel.get(k) for k in parcel_keys]), "\n".join(grantors), "\n".join(grantees), document_number)

        print(row)
        writer.writerow(row)
