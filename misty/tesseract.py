import base64
import logging
import os
import re
from io import BytesIO

import pdf2image
import pytesseract

from config import CORPUS_BASEDIR, TESSERACT_BIN
from misty.__main__ import freenode_OnlineCop_re
from misty.utils import print_and_say


# windows?
# tesseract https://github.com/UB-Mannheim/tesseract/wiki
# poppler https://blog.alivate.com.au/poppler-windows/
# copy some place, modify system to include bin folder in PATH
# TODO: configure location for poppler

def pil_to_b64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())


def ocrpdf(path):
    images = pdf2image.convert_from_path(path)
    for image in images:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_BIN
        text = pytesseract.image_to_string(image)
        yield image, text.strip()


def ocrdir(basedir):
    if not os.path.isfile(TESSERACT_BIN):
        logging.critical("You must install tesseract for OCR.")

    for basename in os.listdir(CORPUS_BASEDIR):
        path = os.path.join(CORPUS_BASEDIR, basename)

        if os.path.isdir(path):
            continue

        name, ext = os.path.splitext(basename)
        ext = ext.lower()
        if ext == '.pdf':
            for n, (image, text) in enumerate(ocrpdf(path)):
                image_path = os.path.join(basedir, f"{name}-{n}.jpg")
                if os.path.exists(image_path):
                    continue

                image.save(image_path, 'JPEG')

                print(text)

                matches = re.finditer(freenode_OnlineCop_re, text)
                for n, match in enumerate(matches, start=1):
                    prefix, title, punctuation, body = match.groups()
                    line = match.group(0)
                    logging.debug(n, prefix, title)
                    print_and_say(title)
                    # wav_out = os.path.join(sec_dir, f'{n}-{slugify(title)}.wav')
                    # if not os.path.exists(wav_out):
                    #     tts.save_to_file(line, wav_out)
                    #     tts.runAndWait()

                # image.show()


if __name__ == '__main__':
    ocrdir(CORPUS_BASEDIR)
