import csv

from sacass import get_eproptax

# from members import apns

apns = [20111700180000, 20111700230024, 20111700250024, 20111700270024, 20111700240013, 20111700280024, 20111700190000,
        20111700220017, 20111700260024, 20111700170013]

with open('taxes.csv', 'w', newline='') as fh:
    writer = csv.writer(fh, dialect=csv.excel_tab)

    for apn in apns:
        eproptax = get_eproptax(apn)

        keys = [
            'ParcelNumber',
            'Address',
            'IsDelinquent',
        ]
        row = (*tuple([eproptax['GlobalData'].get(k) for k in keys]),
               sum([float(bill['BillAmount']) for bill in eproptax['Bills']]))

        print(row)
        writer.writerow(row)
