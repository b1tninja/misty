#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# wget -r -c -np -l 1 -A zip downloads.leginfo.legislature.ca.gov
# --path should be a directory containing pubinfo_2021.zip, defaults to downloads.leginfo.legislature.ca.gov

import datetime
import io
import json
import logging
import os
import os.path
import pprint
import sys
import zipfile
from contextlib import closing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

ENCODING = 'utf-8'
CURRENT_YEAR = datetime.datetime.today().year

# Instead of importing bcolors, just stole the dictionary. Props to Yogesh Sharma
ansi_escape_codes = {'OK': '\x1b[92m',
                     'WARN': '\x1b[93m',
                     'ERR': '\x1b[31m',
                     'UNDERLINE': '\x1b[4m',
                     'ITALIC': '\x1b[3m',
                     'BOLD': '\x1b[1m',
                     'BLUE': '\x1b[94m',
                     'ENDC': '\x1b[0m',
                     'HEADER': '\x1b[95m\x1b[1m',
                     'PASS': '\x1b[92m\x1b[1m',
                     'FAIL': '\x1b[31m\x1b[1m',
                     'HELP': '\x1b[93m',
                     'BITALIC': '\x1b[1m\x1b[3m',
                     'BLUEIC': '\x1b[1m\x1b[3m\x1b[92m',
                     'END': '\x1b[0m'}

try:
    import html2text
except:
    logger.error(
        "Aaron Swartz's python-html2text failed to load, may need to be installed to parse HTML/CAML into MarkDown/plain-text.")
    html2text = False


def opt_tqdm(iterable):
    """
    Optional tqdm progress bars
    """
    try:
        import tqdm
    except:
        return iterable
    else:
        return tqdm.tqdm(iterable)


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


def get_dats_and_lobs(path, prefixes=None):
    """gotta get dats... and lobs"""
    # https://youtu.be/IC9nuBmeX-A
    basename = os.path.basename(path)
    dats = dict()
    lobs = dict()

    logger.info("Extracting dats and lobs from: %s", basename)
    with zipfile.ZipFile(path) as zf:
        for file in opt_tqdm(zf.filelist):
            name, ext = os.path.splitext(file.filename)
            if type(prefixes) is list and not any([file.filename.startswith(p) for p in prefixes]):
                logger.debug("Skipping: %s", file.filename)
                continue

            if ext == '.dat':
                dats[name] = list(read_rows_from_zipped(zf, file))

            elif ext == '.lob':
                CAML = read_text_from_zipped_file(zf, file.filename)
                if html2text:
                    lobs[file.filename] = html2text.HTML2Text(bodywidth=0).handle(CAML)
                else:
                    lobs[file.filename] = CAML
            else:
                logger.debug("Unhandled content: %s", file.filename)

    return dats, lobs


def unzip_dats_and_lobs(path, jsonp=False, **kwargs):
    assert os.path.isfile(path)

    pubinfo = None
    json_path = path + '.jsonp'

    if jsonp and os.path.exists(json_path):
        assert os.path.isfile(json_path)
        with closing(open(json_path, 'r', encoding=ENCODING)) as fh:
            try:
                pubinfo = json.load(fh)
            except (json.JSONDecodeError, IOError):
                pass

    if pubinfo is None:
        dats, lobs = get_dats_and_lobs(path, **kwargs)
        pubinfo = dict(dats=dats, lobs=lobs)

        if jsonp:
            logger.info('Writting json version of dats and lobs found "%s" to "%s".', path, os.path.basename(json_path))
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


def datetime_fromiso(dt):
    return datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')


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
    TRANS_UPDATE = datetime_fromiso(TRANS_UPDATE)
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
    TRANS_UPDATE = datetime_fromiso(TRANS_UPDATE)
    return dict(**locals())


@starg
def LawSectionTblDict(PK, LAW_CODE, SECTION_NUM, OP_STATUES, OP_CHAPTER, OP_SECTION, EFFECTIVE_DATE,
                      LAW_SECTION_VERSION_ID, DIVISION, TITLE, PART, CHAPTER, ARTICLE, HISTORY, LOB_FILE, ACTIVE_FLG,
                      TRANS_UID, TRANS_UPDATE):
    # NOTE: changed ID to PK to avoid conflict with whoosh.fields.ID
    if EFFECTIVE_DATE is not None:
        EFFECTIVE_DATE = datetime_fromiso(EFFECTIVE_DATE)  # .date()

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

    TRANS_UPDATE = datetime_fromiso(TRANS_UPDATE)

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
                     LAW=LOB,
                     SECTION_TITLE=code_section_titles[LAW_CODE].get(SECTION_NUM, {}).get('TITLE'),
                     SECTION_HISTORY=HISTORY)

        except:
            logger.warning("Unexpected table structure, unsure how to format law section: ", LAW_CODE, DIVISION, CHAPTER, ARTICLE, SECTION_NUM)
            pprint.pprint(LawSectionTblDict(law_section))

        else:
            yield d


def index_pubinfos(basedir):
    """whoosh fulltext search index of the pubinfo, currently each individual section from  the CODES/LAW table"""
    from misty.whoosh import Indexer

    indexer = Indexer()
    for path, (dats, lobs) in get_datses_and_lobses(basedir, prefixes=['LAW', 'CODE']):
        logger.info("Pubinfo zip: %s", path)
        try:
            laws = parse_datlobs(lobs, **dats)
            indexer.index_pubinfo_laws(path, laws)

        except TypeError as e:
            logger.warning("Skipping %s... %s.", path, e)
    else:
        logger.info("No more pubinfo_*.zip(s) to index in %s", basedir)


def print_pubinfos(basedir, colorize=False, jsonp=False):
    """Print pubinfo laws directly from odd-year pubinfos"""
    # First replace the ANSI terminal codes in the format string for colorized output
    law_fmt = \
"""
{BLUE}{{CODE_HEADING}}{ENDC}
    {{DIVISION_HEADING}}
        {{CHAPTER_HEADING}}

{UNDERLINE}{{ARTICLE_HEADING}}{ENDC} ( {ITALIC}{{ARTICLE_HISTORY}}{ENDC} )

{BOLD}{{SECTION_TITLE}}{ENDC}
{{LAW}}
{ITALIC}{{SECTION_HISTORY}}{ENDC}
""".format_map(ansi_escape_codes if colorize else dict([(k, '') for k in ansi_escape_codes.keys()]))

    for path, (dats, lobs) in get_datses_and_lobses(basedir, prefixes=['LAW', 'CODE'], jsonp=jsonp):
        logger.info("Pubinfo zip: %s", path)
        try:
            for law in parse_datlobs(lobs, **dats):
                print(law_fmt.format(**law))

        except TypeError as e:
            logger.warning("Skipping %s... %s.", path, e)
    else:
        logger.info("No more pubinfo_*.zip(s) to index in dir: %s", basedir)


def dir_path(path):
    logger.info("Checking --path: %s", path)
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='downloads.leginfo.legislature.ca.gov pubinfo_*.zip Code reader.')
    parser.add_argument('--path', type=dir_path,
                        default='downloads.leginfo.legislature.ca.gov',
                        help="Path of directory containing pubinfo_2021.zip from downloads.leginfo.legislature.ca.gov")
    # TODO: downloader
    # parser.add_argument('-d', '--download', action=argparse.BooleanOptionalAction)
    # parser.add_argument('-i', '--index', action=argparse.BooleanOptionalAction)
    try:
        parser.add_argument('-c', '--color', action=argparse.BooleanOptionalAction, default=False)
        parser.add_argument('-j', '--json', action=argparse.BooleanOptionalAction, default=False, help="Export laws/codes into a .json per pubinfo by parsing the dats and lobs")
    except:
        parser.add_argument('-c', '--color', action="store_true")
        parser.add_argument('-j', '--json', action="store_true")
    # TODO: colorize should only be used with --plaintext
    # parser.add_argument('query', nargs=argparse.REMAINDER)

    try:
        args = parser.parse_args()
    except NotADirectoryError:
        logger.critical("Please specify a path to a directory containing pubinfo_2021.zip")
        parser.print_help(sys.stderr)
    else:
        # TODO: hook whoosh indexer back up, removed temporarily to eliminate dependencies
        # if args.index:
        #     index_pubinfos()

        print_pubinfos(args.path, colorize=args.color, jsonp=args.json)
