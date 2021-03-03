import logging

from .ca import color_law_fmt
from .config import CORPUS_BASEDIR, TTS_BASEDIR
from .utils import print_and_say, mkdir, query
from .whoosh import Indexer

logger = logging.getLogger('misty')


def main():
    # TODO: argparse.ArgumentParser()
    mkdir(CORPUS_BASEDIR)
    mkdir(TTS_BASEDIR)
    indexer = Indexer()
    # indexer.refresh_index(CORPUS_BASEDIR)

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

        # indexer.search_txt(q, print_results)

        def print_law_results(results):
            nonlocal q

            if not results:
                print_and_say(f"No hits for {q}.")
            else:
                print_and_say(f"{len(results)} hits for: {q}.")

                for result in results:
                    print(color_law_fmt.format(**result))

        indexer.search_law(q, print_law_results)


if __name__ == '__main__':
    main()
