import logging
import os.path
from enum import Enum, auto

from whoosh import highlight, index
from whoosh.fields import SchemaClass, ID, TEXT, NUMERIC, KEYWORD
from whoosh.qparser import QueryParser

from .config import WHOOSH_INDEX_BASEDIR
from .tesseract import ocrpdf
from .utils import mkdir, parse_document, for_file_path_name_by_ext, save_txt

logger = logging.getLogger(os.path.basename(__file__))


class TxtSchema(SchemaClass):
    path = ID(stored=True, unique=True)
    name = TEXT(stored=True)
    section = TEXT(stored=True)
    content = TEXT(stored=True)
    line = NUMERIC(stored=True)


class LawSchema(SchemaClass):
    CODE = KEYWORD(stored=True)
    DIVISION = ID(stored=True)
    TITLE = ID(stored=True)
    CHAPTER = ID(stored=True)
    ARTICLE = ID(stored=True)
    ARTICLE_HISTORY = TEXT(stored=True)
    SECTION_NUM = NUMERIC(stored=True)
    LEGAL_TEXT = TEXT(stored=True)
    SECTION_HISTORY = TEXT(stored=True)
    OP_STATUTE = ID(stored=True)
    OP_CHAPTER = ID(stored=True)


class IndexState(Enum):
    Unknown = auto()
    Created = auto()
    Initialize = auto()
    Opening = auto()
    Opened = auto()
    Committed = auto()


class Indexer:
    def __init__(self, basedir=WHOOSH_INDEX_BASEDIR):
        self.state = IndexState.Unknown

        self.txt_idx_path = os.path.join(basedir, 'documents')
        self.law_idx_path = os.path.join(basedir, 'documents')

        if any([not os.path.exists(d) for d in [basedir, self.txt_idx_path, self.law_idx_path]]):
            self.state = IndexState.Initialize

        mkdir(basedir)

    def index_txt(self, path):
        document = parse_document(path)
        self.index_parsed_document(document)

    def index_pdf(self, path):
        file_name = os.path.basename(path)
        name, ext = os.path.splitext(file_name)

        img_dir = os.path.join(os.path.dirname(path), name)
        image_texts = list(ocrpdf(path))
        for page_num, (image, text) in enumerate(image_texts):
            img_path = os.path.join(img_dir, f"{page_num}.jpg")
            image.save(img_path)

            txt_path = os.path.join(img_dir, f"{page_num}.txt")
            save_txt(txt_path, text)

        document = dict(path=path,
                        name=name,
                        sections=dict(
                            [(f"Page {i}", txt) for i, (img, txt) in enumerate(image_texts)]
                        ))
        self.index_parsed_document(document)

    def refresh_index(self, basedir, remove_deleted=False):
        # Index corpus
        for path, name, file_name, ext in for_file_path_name_by_ext(basedir, ['txt', 'pdf']):
            if ext == 'txt':
                document = parse_document(path)
                logger.info(f"Parsed {file_name} into {len(document['sections'])} sections.")
                self.index_parsed_document(document)
            if ext == 'pdf':
                self.index_pdf(path)
            # TODO: .jpg

        ix = self.txt_idx = index.open_dir(self.txt_idx_path)
        with ix.searcher() as searcher:
            # Loop over the stored fields in the index
            indexed_paths = set([fields['path'] for fields in searcher.all_stored_fields()])

        if remove_deleted:
            raise NotImplementedError()
            writer = ix.writer()
            writer.commit()

    def index_parsed_document(self, document):
        if mkdir(self.txt_idx_path):
            txt_idx = index.create_in(self.txt_idx_path, TxtSchema)
        else:
            txt_idx = index.open_dir(self.txt_idx_path)

        with txt_idx.writer() as writer:
            for n, (section, lines) in enumerate(document['sections'].items(), start=1):
                if section is None:
                    section = document['name']
                # else:
                #     print_and_say(section, print_prefix=f"{n}.\t")

                for l, line in enumerate(lines):
                    writer.add_document(path=document['path'],
                                        name=document['name'],
                                        section=section,
                                        line=l,
                                        content=line)

    def index_law_section(self, law_section):
        pass

    def search(self, q, result_cb):
        idx = index.open_dir(self.txt_idx_path)
        with idx.searcher() as searcher:
            parser = QueryParser("content", idx.schema).parse(q)
            results = searcher.search(parser)
            # results.fragmenter = highlight.PinpointFragmenter(surround=64, autotrim=True)
            results.fragmenter = highlight.ContextFragmenter(surround=128)
            results.formatter = highlight.UppercaseFormatter()
            result_cb(results)

    def index_codes(self, *args, **kwargs):
        pass
