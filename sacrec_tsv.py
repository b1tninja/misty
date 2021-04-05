import csv
import json
import logging
import os
from operator import itemgetter

from tqdm import tqdm


# TODO: don't initialize params with mutables, use None
def lod2csv(path, rows,
            group_by='ID',
            ignore=None,
            sort_by=None,
            reprs=None):
    """list of dictionaries to CSV"""
    if ignore is None:
        ignore = list()

    if reprs is None:
        reprs = dict()

    keys = rows[0].keys()  # TODO: set([r.keys() for r in l]), bonus points for next()/iter

    ud = dict([(int(o[group_by]), o) for o in rows]) if group_by else enumerate(rows)
    with open(path, 'w') as fh:
        dw = csv.DictWriter(fh, [k for k in keys if k not in ignore], delimiter='\t')
        dw.writeheader()
        dw.writerows([dict(((k, reprs.get(k, lambda v: v)(v)) for k, v in r.items() if k not in ignore)) for r in
                      (sorted(ud.values(), key=itemgetter(sort_by)) if sort_by else rows)])


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

        if not rows:
            logging.warning("No rows!")
            continue

        csv_name = name + '.csv'
        csv_path = os.path.join(root_dir, csv_name)

        lod2csv(csv_path, rows,
                group_by='ID',
                sort_by='PrimaryDocNumber',
                ignore=['ID', 'SecondaryDocNumber', 'FilingCode', 'BookNumber', 'NumberOfPages', 'BookType'],
                reprs={'Names': lambda v: '|'.join(v.split("<br/>"))})
