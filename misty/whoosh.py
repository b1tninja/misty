import logging
import os.path
from enum import Enum, auto

from whoosh import highlight, index
from whoosh.fields import SchemaClass, ID, TEXT, NUMERIC
from whoosh.qparser import QueryParser

from .config import WHOOSH_INDEX_BASEDIR
from .utils import mkdir, parse_document

logger = logging.getLogger(os.path.basename(__file__))


class TxtSchema(SchemaClass):
    path = ID(stored=True)
    name = TEXT(stored=True)
    section = TEXT(stored=True)
    content = TEXT(stored=True)
    line = NUMERIC(stored=True)


class LawSchema(SchemaClass):
    CODE = 1
    DIVISION = 2
    TITLE = 3
    CHAPTER = 4
    ARTICLE = 5
    SECTION_NUM = 6
    TEXT = 7
    HISTORY = 8
    OP_STATUTE = 9
    OP_CHAPTER = 10


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

    def index_document(self, path):
        document = parse_document(path)
        self.index_parsed_document(document)

    def incremental_index(self, dirname):
        # The set of all paths in the index
        indexed_paths = set()
        # The set of all paths we need to re-index
        to_index = set()

        ix = self.txt_idx = index.open_dir(self.txt_idx_path)
        with ix.searcher() as searcher:
            writer = ix.writer()

            # Loop over the stored fields in the index
            for fields in searcher.all_stored_fields():
                indexed_path = fields['path']
                indexed_paths.add(indexed_path)

                if not os.path.exists(indexed_path):
                    # This file was deleted since it was indexed
                    writer.delete_by_term('path', indexed_path)

                else:
                    # Check if this file was changed since it
                    # was indexed
                    indexed_time = fields['time']
                    mtime = os.path.getmtime(indexed_path)
                    if mtime > indexed_time:
                        # The file has changed, delete it and add it to the list of
                        # files to reindex
                        writer.delete_by_term('path', indexed_path)
                        to_index.add(indexed_path)

            # Loop over the files in the filesystem
            # Assume we have a function that gathers the filenames of the
            # documents to be indexed
            for path in my_docs():
                if path in to_index or path not in indexed_paths:
                    # This is either a file that's changed, or a new file
                    # that wasn't indexed before. So index it!
                    add_doc(writer, path)

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
