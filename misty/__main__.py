import logging
import os

from .config import CORPUS_BASEDIR, TTS_BASEDIR
from .utils import print_and_say, mkdir, query, parse_document
from .whoosh import Indexer

logger = logging.getLogger('misty')


def for_path_name_is_file_in(basedir):
    for name in os.listdir(basedir):
        path = os.path.join(basedir, name)
        is_file = os.path.isfile(path)
        yield path, name, is_file


def for_file_path_name_ext_in(basedir):
    for path, name, is_file in for_path_name_is_file_in(basedir):
        if not is_file:
            continue

        file_name, ext = os.path.splitext(name)

        assert ext[0] == '.'
        yield path, name, file_name, ext[1:].lower()


def for_file_path_name_by_ext(basedir, ext):
    if type(ext) is list:
        ext = list(map(str.lower, ext))

    for path, name, file_name, file_ext in for_file_path_name_ext_in(basedir):
        assert type(ext) in [list, str]
        if type(ext) is str and file_ext.lower() != ext.lower():
            continue

        elif type(ext) is list and file_ext not in ext:
            continue

        yield path, name, file_name, file_ext


def main():
    # TODO: argparse.ArgumentParser()
    mkdir(CORPUS_BASEDIR)
    mkdir(TTS_BASEDIR)
    indexer = Indexer()

    # Index corpus
    for path, name, file_name, ext in for_file_path_name_by_ext(CORPUS_BASEDIR, ['txt', 'pdf']):
        if ext == 'txt':
            document = parse_document(path)
            logger.info(f"Parsed {file_name} into {len(document['sections'])} sections.")
            indexer.index_parsed_document(document)
        # TODO: .pdf
        # TODO: .jpg

    ################################ QUERY ################################
    while True:
        q = query()
        if not q or q is True:
            continue

        # Qquit
        elif q.lower() in 'Qq':
            break

        def print_results(results):
            nonlocal q

            if not results:
                print_and_say(f"No hits for {q}.")
            else:
                print_and_say(f"{len(results)} hits for: {q}.")

                grouped_results = dict()
                for result in results:
                    grouped_results.setdefault((result.get('name')),
                                               dict()).setdefault(result.get('section'),
                                                                  list()).append(result)

                for j, (file_name, sections) in enumerate(grouped_results.items(), start=1):
                    print_and_say(f"Document {j}. {file_name}")

                    for k, (section, results) in enumerate(sections.items(), start=1):
                        print_and_say(section, print_prefix=f"\t{j}\tSection {k}.\t")

                        for result in sorted(results, key=lambda result: result.get('line')):
                            highlights = result.highlights("content")

                            for line in highlights.split("\n"):
                                if line:
                                    print_and_say(line, print_prefix="\t\t\t")

        indexer.search(q, print_results)


if __name__ == '__main__':
    main()
