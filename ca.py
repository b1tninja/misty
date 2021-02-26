import base64
import datetime
import io
import json
import logging
import os
import zipfile
from contextlib import closing

import html2text
import tqdm

LEGINFO_BASEDIR = r"D:\downloads.leginfo.legislature.ca.gov"
ENCODING = 'utf-8'


# wget --mirror https://downloads.leginfo.legislature.ca.gov/


def read_text_from_zipped_file(zip_file, target):
    with io.TextIOWrapper(zip_file.open(target, 'r'), encoding=ENCODING) as text_file:
        return text_file.read()


def read_lines_from_zipped_file(zip_file, target):
    with io.TextIOWrapper(zip_file.open(target, 'r'), encoding=ENCODING) as text_file:
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


def get_dats_and_lobs(path, prefixes=None, txt=True):
    basename = os.path.basename(path)
    dats = dict()
    lobs = dict()

    print(f"Extracting dats and lobs from {basename}...")
    with zipfile.ZipFile(path) as zf:
        for file in tqdm.tqdm(zf.filelist):
            name, ext = os.path.splitext(file.filename)
            if type(prefixes) is list and not any([file.filename.startswith(p) for p in prefixes]):
                logging.debug(f"Skipping {file.filename}...")
                continue

            if ext == '.dat':
                dats[name] = list(read_rows_from_zipped(zf, file))

            elif ext == '.lob':
                if txt:
                    html2txt = html2text.HTML2Text(bodywidth=0)
                    html = read_text_from_zipped_file(zf, file.filename)
                    TEXT = html2txt.handle(html)
                    lobs[file.filename] = TEXT
                else:
                    lobs[file.filename] = base64.b64encode(zf.read(file.filename))
            else:
                logging.debug(f"Unhandled content: {file.filename}")

    return dats, lobs


def get_pubinfo(path):
    assert os.path.isfile(path)
    json_path = path + '.json'

    pubinfo = None
    if os.path.exists(json_path):
        assert os.path.isfile(json_path)
        with closing(open(json_path, 'r', encoding=ENCODING)) as fh:
            try:
                pubinfo = json.load(fh)
            except (json.JSONDecodeError, IOError):
                pubinfo = None

    if pubinfo is None:
        dats, lobs = get_dats_and_lobs(path, prefixes=['LAW', 'CODE'])
        pubinfo = dict(dats=dats, lobs=lobs)

        logging.info(f'Writting json version of dats and lobs found "{path}" to "{os.path.basename(json_path)}".')

        with closing(open(json_path, 'w', encoding=ENCODING)) as fh:
            try:
                json.dump(pubinfo, fh)  # ensure_ascii=True
            except UnicodeEncodeError as e:
                logging.warning("Not Plain-Text:", e)
            except Exception as e:
                logging.critical("Unable to write pubinfo JSON to disk", e)

    return pubinfo


def get_pubinfos(basedir):
    for basename in os.listdir(basedir):
        if not basename.endswith('.zip'):
            continue

        path = os.path.join(basedir, basename)

        if not os.path.isfile(path):
            continue

        pubinfo = get_pubinfo(path)
        yield path, pubinfo


# def dedat(func, *args, **kwargs):
#     return func(*args, **dict([(os.path.splitext(k)[0], v) for k, v in kwargs.items()])
#
# @dedat
def parse_dats(*, CODES_TBL, LAW_TOC_TBL, LAW_SECTION_TBL, LAW_TOC_SECTIONS_TBL, **dats):
    if not all([r + '.dat' in dats for r in locals()]):
        logging.warning(f"Skipping {path}... missing required sections.")
        return


if __name__ == '__main__':
    for path, pubinfo in get_pubinfos(LEGINFO_BASEDIR):

        dats = pubinfo['dats']
        lobs = pubinfo['lobs']

        required = ['CODES_TBL', 'LAW_SECTION_TBL', 'LAW_TOC_SECTIONS_TBL']
        parse_dats(**dict([(os.path.splitext(k)[0], v) for k, v in dats.items()]))

        codes_tbl = dict(dats['CODES_TBL.dat'])

        for row in dats.get('LAW_TOC_TBL.dat', []):
            LAW_CODE, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HEADING, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE, NODE_SEQUENCE, NODE_LEVEL, NODE_POSITION, NODE_TREEPATH, CONTAINS_LAW_SECTIONS, HISTORY_NOTE, OP_STATUES, OP_CHAPTER, OP_SECTION = row
            # print(HEADING)
            print(row)

        for row in dats.get('LAW_TOC_SECTIONS_TBL.dat', []):
            ID, LAW_CODE, NODE_TREEPATH, SECTION_NUM, SECTION_ORDER, TITLE, OP_STATUES, OP_CHAPTER, OP_SECTION, TRANS_UID, TRANS_UPDATE, LAW_SECTION_VERSION_ID, SEQ_NUM = row
            # print(LAW_CODE, NODE_TREEPATH, SECTION_NUM, SECTION_ORDER)
            print(row)

        codes = dict()
        for row in dats.get('LAW_SECTION_TBL.dat', []):
            ID, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE, LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE = row
            if EFFECTIVE_DATE is not None:
                EFFECTIVE_DATE = datetime.datetime.fromisoformat(EFFECTIVE_DATE).date()

            print(row)

            TEXT = lobs.get(LOB_FILE)
            print(TEXT)

            codes.setdefault(LAW_CODE, dict())
            codes[LAW_CODE].setdefault(OP_SECTION, dict())
            codes[LAW_CODE][OP_SECTION][ID] = TEXT
