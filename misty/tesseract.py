import base64
import logging
import os
from contextlib import closing
from io import BytesIO

import pytesseract
import tqdm

from .config import CORPUS_BASEDIR, TESSERACT_BIN
from .utils import mkdir


def pil_to_b64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())


def image_to_text(image):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_BIN
    text = pytesseract.image_to_string(image)
    return text


def ocrpdf(path):
    return
    logging.info(f"Extracting page images from {path}")
    logging.info("Using neural network to identify lines, and convert graphemes into text.")
    for image in tqdm.tqdm(pdf2image.convert_from_path(path)):
        image_to_text(image)
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

            # TODO: multiprocessing tqdm, or some way to read the pagination as a first step
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


def pdf_page_image(path, page):
    raise NotImplementedError()
    import pdf2image
    return list(pdf2image.convert_from_path(path))
