import csv
import os.path
from datetime import date

from sacass import get_eproptax, download_taxbill, download_paymentstub

apns = [20111700180000, 20111700230024, 20111700250024, 20111700270024, 20111700240013, 20111700280024, 20111700190000,
        20111700220017, 20111700260024, 20111700170013]

# from members import apns

if __name__ == '__main__':
    taxes = 0.0
    year = date.today().strftime('%y')
    tax_dir = 'taxes/'
    os.makedirs(tax_dir, exist_ok=True)

    with open('taxes.csv', 'w', newline='') as fh:
        writer = csv.writer(fh, dialect=csv.excel_tab)
        keys = [
            'ParcelNumber',
            'Address',
            'IsDelinquent',
        ]

        for apn in apns:
            eproptax = get_eproptax(apn)

            for bill in eproptax['Bills']:
                bill_number = year + bill['BillNumber']

                dst = os.path.join(tax_dir, "Bill %s-%s.pdf" % (apn, bill_number))
                download_taxbill('23' + bill['BillNumber'], dst)  # YY+bill

                dst = os.path.join(tax_dir, "PaymentStub %s-%s.pdf" % (apn, bill_number))
                download_paymentstub(apn, '2023' + bill['BillNumber'] + '12', dst)  # YYYY+bill+installments

            row = (*tuple([eproptax['GlobalData'].get(k) for k in keys]),
                   sum([float(bill['BillAmount']) for bill in eproptax['Bills']]))

            taxes += row[-1]

            print(row)
            writer.writerow(row)

    print(taxes)
