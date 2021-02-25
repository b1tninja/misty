import datetime
import io
import json
import os
import zipfile

import tqdm

LEGINFO_BASEDIR = r"D:\downloads.leginfo.legislature.ca.gov"


# wget --mirror https://downloads.leginfo.legislature.ca.gov/


def read_text_from_zipped_file(zip_file, target):
    with io.TextIOWrapper(zip_file.open(target, 'r'), encoding="utf-8") as text_file:
        return text_file.read()


def read_lines_from_zipped_file(zip_file, target):
    with io.TextIOWrapper(zip_file.open(target, 'r'), encoding="utf-8") as text_file:
        for line in map(str.rstrip, iter(text_file.readline, '')):
            if not line:
                continue

            yield line


def read_rows_from_zipped(zip_file, target):
    for line in read_lines_from_zipped_file(zip_file, target):
        if not line:
            continue

        row = line.split("\t")
        yield tuple(col[1:-1] if col[0] == col[-1] == '`' else
                    None if col == 'NULL' else
                    col for col in row)


import html2text

for basename in os.listdir(LEGINFO_BASEDIR):
    dats = dict()
    lobs = dict()

    if not basename.endswith('.zip'):
        continue

    path = os.path.join(LEGINFO_BASEDIR, basename)
    if not os.path.isfile(path):
        continue

    print(f"Extracting {os.path.basename(path)}...")
    with zipfile.ZipFile(path) as zf:
        for file in tqdm.tqdm(zf.filelist):
            if not any([file.filename.startswith(p) for p in ['LAW', 'CODE']]):
                continue

            if file.filename.endswith('.dat'):
                dats[file.filename] = list(read_rows_from_zipped(zf, file))

            elif file.filename.endswith('.lob'):
                html2txt = html2text.HTML2Text(bodywidth=0)
                html = read_text_from_zipped_file(zf, file.filename)
                TEXT = html2txt.handle(html)
                lobs[file.filename] = TEXT

    for row in dats.get('LAW_TOC_TBL.dat', []):
        LAW_CODE, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HEADING, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE, NODE_SEQUENCE, NODE_LEVEL, NODE_POSITION, NODE_TREEPATH, CONTAINS_LAW_SECTIONS, HISTORY_NOTE, OP_STATUES, OP_CHAPTER, OP_SECTION = row
        # print(row)

    for row in dats.get('LAW_TOC_SECTIONS_TBL.dat', []):
        ID, LAW_CODE, NODE_TREEPATH, SECTION_NUM, SECTION_ORDER, TITLE, OP_STATUES, OP_CHAPTER, OP_SECTION, TRANS_UID, TRANS_UPDATE, LAW_SECTION_VERSION_ID, SEQ_NUM = row
        # print(TITLE)

    codes = dict()
    for row in dats.get('LAW_SECTION_TBL.dat', []):
        ID, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE, LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE = row
        if EFFECTIVE_DATE is not None:
            EFFECTIVE_DATE = datetime.datetime.fromisoformat(EFFECTIVE_DATE).date()

        TEXT = lobs.get(LOB_FILE)

        codes.setdefault(LAW_CODE, dict())
        codes[LAW_CODE].setdefault(OP_SECTION, dict())
        codes[LAW_CODE][OP_SECTION][ID] = TEXT

    else:

        with open(os.path.join(LEGINFO_BASEDIR, basename + '.json'), 'w') as fh:
            json.dump(codes, fh)
