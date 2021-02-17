import os


CORPUS_BASEDIR = os.path.join(os.path.dirname(__file__), 'corpus')
TTS_BASEDIR = CORPUS_BASEDIR
WHOOSH_INDEX_BASEDIR = os.path.join(CORPUS_BASEDIR, 'whoosh')