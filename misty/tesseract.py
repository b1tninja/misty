import base64
import logging
import os
from contextlib import closing
from io import BytesIO

import pdf2image
import pytesseract
import tqdm

from config import CORPUS_BASEDIR, TESSERACT_BIN
from misty.utils import mkdir


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
    logging.info(f"Extracting page images from {path}")
    images = list(pdf2image.convert_from_path(path))
    logging.info("Using neural network to recognize text")
    for image in tqdm.tqdm(images):
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
            pdfoutdir = os.path.join(basedir, name)
            if not mkdir(pdfoutdir):
                continue

            for n, (image, text) in enumerate(ocrpdf(path)):
                image_path = os.path.join(pdfoutdir, f"{n}.jpg")

                if os.path.exists(image_path):
                    continue
                else:
                    image.save(image_path, 'JPEG')

                txt_path = os.path.join(pdfoutdir, f"{n}.txt")
                if not os.path.exists(txt_path):
                    with closing(open(txt_path, 'w', encoding='utf-8')) as fh:
                        fh.write(text)

if __name__ == '__main__':
    ocrdir(CORPUS_BASEDIR)
