import os

CORPUS_BASEDIR = os.path.join(os.path.dirname(__file__), 'corpus')
TTS_BASEDIR = os.path.join(os.getcwd(), 'tts')
WHOOSH_INDEX_BASEDIR = os.path.join(os.getcwd(), 'whoosh')

# tesseract https://github.com/UB-Mannheim/tesseract/wiki
TESSERACT_BIN = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# poppler https://blog.alivate.com.au/poppler-windows/
# copy some place, modify system to include bin folder in PATH
# TODO: configure location for poppler
DEFAULT_ENCODING = 'utf-8'
