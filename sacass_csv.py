import csv
import json
import logging
import os
from operator import itemgetter

from tqdm import tqdm


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

    filters = [
        # 'WHIMSICAL LN'
    ]
    filter_by = 'FullAddress'

    rows = [o for o in jsons if not filters or any(v in o[filter_by] for v in filters)]

    if not rows:
        logging.warning("No rows!")

    csv_name = 'rows.csv'
    csv_path = os.path.join(root_dir, csv_name)

    lod2csv(csv_path, rows,
            group_by='APN',
            sort_by='DocumentDate')
