import os
import string
from contextlib import closing

import pyttsx3


from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer

from config import CORPUS_BASEDIR, WHOOSH_INDEX_BASEDIR, TTS_BASEDIR


def readtxt(path):
    # letters = set(string.ascii_letters)

    with closing(open(path, 'r', encoding='utf8')) as fh:
        for line in map(str.strip, iter(fh.readline, '')):
            # if not letters.issubset(line):
            #     continue
            if line == '________________':
                continue
            yield line

class TxtSchema(SchemaClass):
    path = ID(stored=True)
    title = TEXT(stored=True)
    content = TEXT

def title_of(text):
    title, *rest = text.split('.', maxsplit=1)
    return title

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

    letters = set(string.ascii_letters)

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

        for n, line in enumerate(readtxt(path)):
            tts.save_to_file(line, os.path.join(target_dir, '%i-%s.mp3' % (n, title_of(line))))
            tts.runAndWait()
            # tts.say(line)
    else:
        writer.commit()
