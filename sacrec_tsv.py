import csv
import json
import logging
import os
from operator import itemgetter

from tqdm import tqdm

if __name__ == '__main__':
    root_dir = 'sac'
    for name in tqdm(os.listdir(root_dir)):
        path = os.path.join(root_dir, name)

        if not os.path.isdir(path):
            continue

        print('\n', name)

        try:
            jsons = [json.load(open(os.path.join(path, p), 'r')).get('SearchResults') for p in sorted(os.listdir(path))
                     if p.endswith('.json')]
        except json.JSONDecodeError as e:
            logging.error(e)
            continue

        rows = [o for jsonl in jsons for o in jsonl]
        # Make uniq by PrimaryDocNumber and SecondaryDocNumber.
        # TODO: consider frozenset(o.items()) as __hash__
        ud = dict([(int(o['ID']), o) for o in rows])
        desc_rows = [ud[key] for key in sorted(ud.keys(), reverse=True)]

        if not rows:
            logging.warning("No rows!")
            continue

        keys = rows[0].keys()  # TODO: set([r.keys() for r in l]), bonus points for next()/iter

        csv_name = name + '.csv'
        csv_path = os.path.join(root_dir, csv_name)

        sorted(rows, key=itemgetter('PrimaryDocNumber'))

        with open(csv_path, 'w') as fh:
            ignore = ['ID', 'SecondaryDocNumber', 'FilingCode', 'BookNumber', 'NumberOfPages', 'BookType']
            reprs = {'Names': lambda v: '|'.join(v.split("<br/>"))}

            dw = csv.DictWriter(fh, [k for k in keys if k not in ignore], delimiter='\t')
            dw.writeheader()
            dw.writerows([dict(((k, reprs.get(k, lambda v: v)(v)) for k, v in r.items() if k not in ignore)) for r in desc_rows])
