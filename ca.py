import datetime
import io
import json
import logging
import os
import os.path
import pprint
import zipfile
from contextlib import closing
from typing import Optional

import bcolors
import html2text
import tqdm

from misty.whoosh import Indexer

logger = logging.getLogger(os.path.basename(__file__))

# TODO: downloader
# wget --mirror https://downloads.leginfo.legislature.ca.gov/
LEGINFO_BASEDIR = r"D:\downloads.leginfo.legislature.ca.gov"
ENCODING = 'utf-8'
CURRENT_YEAR = datetime.datetime.today().year

law_fmt = """
{CODE_HEADING}
    {DIVISION_HEADING}
        {CHAPTER_HEADING}
{ARTICLE_HEADING} ( {ARTICLE_HISTORY} )

{SECTION_TITLE}
{LEGAL_TEXT}
{SECTION_HISTORY}
"""

color_law_fmt = f"""
{bcolors.BLUE}{{CODE_HEADING}}{bcolors.ENDC}
    {{DIVISION_HEADING}}
        {{CHAPTER_HEADING}}

{bcolors.UNDERLINE}{{ARTICLE_HEADING}}{bcolors.ENDC} ( {bcolors.ITALIC}{{ARTICLE_HISTORY}}{bcolors.ENDC} )

{bcolors.BOLD}{{SECTION_TITLE}}{bcolors.ENDC}
{{LEGAL_TEXT}}
{bcolors.ITALIC}{{SECTION_HISTORY}}{bcolors.ENDC}
"""


class LawLibrary:
    pass


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
                logger.debug(f"Skipping {file.filename}...")
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
                logger.debug(f"Unhandled content: {file.filename}")

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

        logger.info(f'Writting json version of dats and lobs found "{path}" to "{os.path.basename(json_path)}".')

        with closing(open(json_path, 'w', encoding=ENCODING)) as fh:
            try:
                json.dump(pubinfo, fh, ensure_ascii=False)  # ensure_ascii=True
            except UnicodeEncodeError as e:
                logger.warning("Not Plain-Text:", e)
            except Exception as e:
                logger.critical("Unable to write pubinfo JSON to disk", e)

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
def LawSectionTblDict(PK, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE: Optional[str],
                      LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG,
                      TRANS_UID, TRANS_UPDATE):
    # NOTE: changed ID to PK to avoid conflict with whoosh.fields.ID
    if EFFECTIVE_DATE is not None:
        EFFECTIVE_DATE = datetime.datetime.fromisoformat(EFFECTIVE_DATE)  # .date()

    if DIVISION:
        DIVISION = DIVISION.rstrip('.')

    if TITLE:
        TITLE = TITLE.rstrip('.')

    if PART:
        PART = PART.rstrip('.')

    if CHAPTER:
        CHAPTER = CHAPTER.rstrip('.')

    if ARTICLE:
        ARTICLE = ARTICLE.rstrip('.')

    if SECTION_NUM:
        SECTION_NUM = SECTION_NUM.rstrip('.')

    ACTIVE_FLG = 'Y' == ACTIVE_FLG

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

    code_section_titles = dict()
    for d in map(LawTocSectionsTblDict, LAW_TOC_SECTIONS_TBL):
        code_section_titles.setdefault(d['LAW_CODE'],
                                       {}).__setitem__(d['SECTION_NUM'], d)

    codes = dict()
    for law_section in LAW_SECTION_TBL:
        ID, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE, LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG, TRANS_UID, TRANS_UPDATE = law_section
        LOB = LOBS.get(LOB_FILE)
        codes.setdefault(LAW_CODE, dict())
        codes[LAW_CODE].setdefault(OP_SECTION, dict())
        codes[LAW_CODE][OP_SECTION][ID] = LOB

        try:
            d = LawSectionTblDict(law_section)
            d.update(CODE_HEADING=CODES_TBL[LAW_CODE],
                     DIVISION_HEADING=toc_tbl[LAW_CODE][DIVISION][None][None]['HEADING'],
                     CHAPTER_HEADING=toc_tbl[LAW_CODE][DIVISION][CHAPTER][None]['HEADING'],
                     ARTICLE_HEADING=toc_tbl[LAW_CODE][DIVISION][CHAPTER][ARTICLE]['HEADING'],
                     ARTICLE_HISTORY=toc_tbl[LAW_CODE][DIVISION][CHAPTER][ARTICLE]['HISTORY_NOTE'],
                     LEGAL_TEXT=LOB,
                     SECTION_TITLE=code_section_titles[LAW_CODE].get(SECTION_NUM, {}).get('TITLE'),
                     SECTION_HISTORY=HISTORY)

        except:
            logging.warning("Unexpected table structure, unsure how to format LawSe")
            pprint.pprint(LawSectionTblDict(law_section))

        else:
            yield d


def index_pubinfos(basedir=LEGINFO_BASEDIR):
    indexer = Indexer()
    for pubinfo_path, (dats, lobs) in get_datses_and_lobses(basedir, prefixes=['LAW', 'CODE']):
        try:
            laws = parse_datlobs(lobs, **dats)
            indexer.index_pubinfo_laws(pubinfo_path, laws)

        except TypeError as e:
            logger.warning(f"Skipping {pubinfo_path}... {e}.")


def print_pubinfos(basedir=LEGINFO_BASEDIR):
    for path, (dats, lobs) in get_datses_and_lobses(basedir, prefixes=['LAW', 'CODE']):
        try:
            for law in parse_datlobs(lobs, **dats):
                print(law_fmt.format(**law))

        except TypeError as e:
            logger.warning(f"Skipping {path}... {e}.")


if __name__ == '__main__':
    index_pubinfos()
