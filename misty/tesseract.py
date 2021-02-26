import logging
import os

import pdf2image
import pytesseract

from config import CORPUS_BASEDIR, TESSERACT_BIN
from misty.utils import print_and_say


def ocr(basedir):
    if not os.path.isfile(TESSERACT_BIN):
        logging.critical("You must install tesseract for OCR.")

    for basename in os.listdir(CORPUS_BASEDIR):
        path = os.path.join(CORPUS_BASEDIR, basename)

        if os.path.isdir(path):
            continue

        name, ext = os.path.splitext(basename)
        ext = ext.lower()
        if ext == '.pdf':
            images = pdf2image.convert_from_path(path)
            for image in images:
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_BIN
                text = pytesseract.image_to_string(image)

                image.show()

                for line in text.split("\n"):
                    print_and_say(line)


if __name__ == '__main__':
    ocr(CORPUS_BASEDIR)
