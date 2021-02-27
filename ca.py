import datetime
import io
import json
import logging
import os
import zipfile
from contextlib import closing

import bcolors
import html2text
import tqdm

LEGINFO_BASEDIR = r"D:\downloads.leginfo.legislature.ca.gov"
ENCODING = 'utf-8'
CURRENT_YEAR = datetime.datetime.today().year


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


def get_dats_and_lobs(path, prefixes=None, txt=True, width=0):
    """gotta get dats... and lobs"""
    # https://youtu.be/IC9nuBmeX-A
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
                    # Information is power. But like all power, there are those who want to keep it for themselves.
                    html2txt = html2text.HTML2Text(bodywidth=width)
                    html = read_text_from_zipped_file(zf, file.filename)
                    TEXT = html2txt.handle(html)
                    lobs[file.filename] = TEXT
                else:
                    lobs[file.filename] = zf.read(file.filename)
            else:
                logging.debug(f"Unhandled content: {file.filename}")

    return dats, lobs


def unzip_dats_and_lobs(path, **kwargs):
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
        dats, lobs = get_dats_and_lobs(path, **kwargs)
        pubinfo = dict(dats=dats, lobs=lobs)

        logging.info(f'Writting json version of dats and lobs found "{path}" to "{os.path.basename(json_path)}".')

        with closing(open(json_path, 'w', encoding=ENCODING)) as fh:
            try:
                json.dump(pubinfo, fh)  # ensure_ascii=True
            except UnicodeEncodeError as e:
                logging.warning("Not Plain-Text:", e)
            except Exception as e:
                logging.critical("Unable to write pubinfo JSON to disk", e)

    return pubinfo.get('dats', []), pubinfo.get('lobs', [])


def get_datses_and_lobses(basedir, **kwargs):
    for basename in os.listdir(basedir):
        if not basename.endswith('.zip'):
            continue

        path = os.path.join(basedir, basename)

        if not os.path.isfile(path):
            continue

        dats, lobs = unzip_dats_and_lobs(path, **kwargs)
        yield path, (dats, lobs)


def dxt(func):
    return lambda *args, **kwargs: func(*args, **dict([(os.path.splitext(k)[0], v) for k, v in kwargs.items()]))


def starg(func):
    return lambda args: func(*args)


@starg
def LawTocTblDict(LAW_CODE, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HEADING, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE,
                  NODE_SEQUENCE, NODE_LEVEL, NODE_POSITION, NODE_TREEPATH, CONTAINS_LAW_SECTIONS, HISTORY_NOTE,
                  OP_STATUES, OP_CHAPTER, OP_SECTION):
    # if DIVISION:
    #     DIVISION = float(DIVISION.rstrip('.'))
    # if TITLE:
    #     TITLE = int(float(TITLE.rstrip('.')))
    # if PART:
    #     PART = int(float(PART.rstrip('.')))
    # if CHAPTER:
    #     CHAPTER = int(float(CHAPTER.rstrip('.')))
    # if ARTICLE:
    #     ARTICLE = int(float(ARTICLE.rstrip('.')))
    # HEADING
    ACTIVE_FLG = 'Y' == ACTIVE_FLG
    # TRANS_UID
    TRANS_UPDATE = datetime.datetime.fromisoformat(TRANS_UPDATE)
    NODE_SEQUENCE = int(NODE_SEQUENCE)
    NODE_LEVEL = int(NODE_LEVEL)
    NODE_POSITION = int(NODE_POSITION)
    NODE_TREEPATH = tuple(map(int, NODE_TREEPATH.split('.')))
    CONTAINS_LAW_SECTIONS = 'Y' == CONTAINS_LAW_SECTIONS
    # HISTORY_NOTE
    # OP_STATUES = float(OP_STATUES or 0)
    # OP_CHAPTER = float(OP_CHAPTER or 0)
    # OP_SECTION = float(OP_SECTION or 0)

    d = dict(**locals())

    # pprint.pprint(d)
    # assert 1849 <= OP_STATUES <= CURRENT_YEAR

    return d


@starg
def LawTocSectionsTblDict(ID, LAW_CODE, NODE_TREEPATH, SECTION_NUM, SECTION_ORDER, TITLE, OP_STATUES, OP_CHAPTER,
                          OP_SECTION, TRANS_UID, TRANS_UPDATE, LAW_SECTION_VERSION_ID, SEQ_NUM):
    NODE_TREEPATH = tuple(map(int, NODE_TREEPATH.split('.')))
    TRANS_UPDATE = datetime.datetime.fromisoformat(TRANS_UPDATE)
    return dict(**locals())


@starg
def LawSectionTblDict(ID, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE,
                      LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG,
                      TRANS_UID, TRANS_UPDATE):
    EFFECTIVE_DATE = datetime.datetime.fromisoformat(EFFECTIVE_DATE).date()
    TRANS_UPDATE = datetime.datetime.fromisoformat(TRANS_UPDATE)
    return dict(**locals())


@dxt
def parse_datlobs(LOBS, *, CODES_TBL, LAW_TOC_TBL, LAW_SECTION_TBL, LAW_TOC_SECTIONS_TBL):
    CODES_TBL = dict(CODES_TBL)

    # print(next(map(LawTocTblDict, LAW_TOC_TBL)))
    toc_tbl = dict()
    for d in map(LawTocTblDict, LAW_TOC_TBL):
        toc_tbl.setdefault(d['LAW_CODE'],
                           {}).setdefault(d['DIVISION'],
                                          {}).setdefault(d['CHAPTER'],
                                                         {}).__setitem__(d['ARTICLE'], d)

    # toc_tbl[LAW_CODE][DIVISION][CHAPTER][ARTICLE]
    code_section_titles = dict()
    for d in map(LawTocSectionsTblDict, LAW_TOC_SECTIONS_TBL):
        code_section_titles.setdefault(d['LAW_CODE'],
                                       {}).__setitem__(d['SECTION_NUM'], d)

    codes = dict()
    for ID, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE, LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE in LAW_SECTION_TBL:
        LOB = LOBS.get(LOB_FILE)
        codes.setdefault(LAW_CODE, dict())
        codes[LAW_CODE].setdefault(OP_SECTION, dict())
        codes[LAW_CODE][OP_SECTION][ID] = LOB

        # o = io.StringIO()
        # o.writelines([])
        _toc = toc_tbl[LAW_CODE][DIVISION][CHAPTER][ARTICLE]
        print(f"{bcolors.BLUE}{CODES_TBL[LAW_CODE]}{bcolors.ENDC}")
        print(f"    {toc_tbl[LAW_CODE][DIVISION][None][None]['HEADING']}")
        print(f"        {toc_tbl[LAW_CODE][DIVISION][CHAPTER][None]['HEADING']}")
        print("")
        print(
            f"{bcolors.UNDERLINE}{_toc['HEADING']}{bcolors.ENDC} ({bcolors.ITALIC}{_toc['HISTORY_NOTE']}{bcolors.ENDC})")
        print(f"        SOMETHING AND THE REST IS ({HISTORY})")
        print("")
        print(f"{bcolors.BOLD}{code_section_titles[LAW_CODE][SECTION_NUM]['TITLE'] or ''}{bcolors.ENDC}")
        print(LOB)

    return codes


if __name__ == '__main__':

    for path, (dats, lobs) in get_datses_and_lobses(LEGINFO_BASEDIR, prefixes=['LAW', 'CODE']):
        # try:
        codes = parse_datlobs(lobs, **dats)
    # except TypeError as e:
    #     logging.warning(f"Skipping {path}... {e}.")
