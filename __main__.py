import os
import re
from contextlib import closing

import pyttsx3
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, ID

from config import CORPUS_BASEDIR, WHOOSH_INDEX_BASEDIR, TTS_BASEDIR

# TODO: strip white space and punctuation from body
freenode_OnlineCop_re = re.compile(r"""
^\s*
(?P<leading_number>[0-9.]+|\([a-z0-9A-Z]+\))?
\s*
(?P<title>
  (?:[^\d.;?\n]+
  |
  \d+(?:\.\d+)?
  )* # Non-digits
)
(?P<punctuation>[.;?,]|$)(?P<body>.*?$)
""", re.MULTILINE | re.VERBOSE)


def readtxt(path):
    with closing(open(path, 'r', encoding='utf8')) as fh:
        for line in map(str.strip, iter(fh.readline, '')):
            if line == '________________':
                continue
            yield line


class TxtSchema(SchemaClass):
    path = ID(stored=True)
    title = TEXT(stored=True)
    content = TEXT


def slugify(s, maxlen=32):
    # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    return "".join(x for x in s if x.isalnum())[:maxlen]


if __name__ == '__main__':
    tts = pyttsx3.init()

    if not os.path.exists(CORPUS_BASEDIR):
        os.mkdir(CORPUS_BASEDIR)
    else:
        assert os.path.isdir(CORPUS_BASEDIR)

    if not os.path.exists(WHOOSH_INDEX_BASEDIR):
        os.mkdir(WHOOSH_INDEX_BASEDIR)
    else:
        assert os.path.isdir(WHOOSH_INDEX_BASEDIR)

    ix = index.create_in(WHOOSH_INDEX_BASEDIR, TxtSchema)
    writer = ix.writer()

    for name in os.listdir(CORPUS_BASEDIR):
        title, ext = os.path.splitext(name)

        if ext.lower() != '.txt':
            continue

        path = os.path.join(CORPUS_BASEDIR, name)

        print(title)

        writer.add_document(title=title, path=path, content="\n".join(readtxt(path)))

        target_dir = os.path.join(TTS_BASEDIR, title)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        else:
            assert os.path.isdir(target_dir)

        matches = re.finditer(freenode_OnlineCop_re, open(path, 'r', encoding='utf8').read())
        for n, match in enumerate(matches, start=1):
            prefix, title, punctuation, body = match.groups()
            line = match.group(0)
            print(n, prefix, title)
            tts.save_to_file(line, os.path.join(target_dir, '%i-%s.mp3' % (n, slugify(title))))
            tts.runAndWait()
    else:
        writer.commit()
