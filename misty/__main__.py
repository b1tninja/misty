import logging
import os
import re

from whoosh import index, highlight
from whoosh.fields import SchemaClass, TEXT, ID, NUMERIC
from whoosh.qparser import QueryParser

from . import voices, tts
from .config import CORPUS_BASEDIR, WHOOSH_INDEX_BASEDIR, TTS_BASEDIR
from .utils import print_and_say, mkdir, slugify, current_speaker, get_sections, query

# TODO: strip white space and punctuation from body
freenode_OnlineCop_re = re.compile(r"""
^\s*
(?P<leading_number>[0-9.]+|\([a-z0-9A-Z]+\))?
\s*
(?P<title>
  (?:[^\d.;?\n]+
  |
  \d+(?:\.\d+(?:[0-9]+\.)*)?
  )* # Non-digits
)
(?P<punctuation>[.;?,]|$)(?P<body>.*?$)
""", re.MULTILINE | re.VERBOSE)


class TxtSchema(SchemaClass):
    path = ID(stored=True)
    document = TEXT(stored=True)
    section = TEXT(stored=True)
    content = TEXT(stored=True)
    line = NUMERIC(stored=True)


def main():
    indexer = None

    mkdir(CORPUS_BASEDIR)
    mkdir(TTS_BASEDIR)

    corpus = dict()
    for name in os.listdir(CORPUS_BASEDIR):
        document, ext = os.path.splitext(name)
        if ext.lower() == '.txt':
            path = os.path.join(CORPUS_BASEDIR, name)
            corpus[document] = path

    if mkdir(WHOOSH_INDEX_BASEDIR):
        # Make Index
        ix = index.create_in(WHOOSH_INDEX_BASEDIR, TxtSchema)
        indexer = ix.writer()
    else:
        assert os.path.isdir(WHOOSH_INDEX_BASEDIR)
        # Read Index
        ix = index.open_dir(WHOOSH_INDEX_BASEDIR)

    for name in os.listdir(CORPUS_BASEDIR):
        document, ext = os.path.splitext(name)

        if ext.lower() != '.txt':
            continue

        path = os.path.join(CORPUS_BASEDIR, name)
        sections = get_sections(path)

        if indexer:
            print_and_say(f'Indexing "{document}".')

            print_and_say(f"Parsed {document} into {len(sections)} sections.")
            for n, (section, lines) in enumerate(sections.items(), start=1):
                # print_and_say(f"{n}.\t{section}")
                for l, line in enumerate(lines):
                    indexer.add_document(path=path,
                                         document=document,
                                         section=section,
                                         line=l,
                                         content=line)

        for voice in voices.values():
            tts.runAndWait()
            tts.setProperty('voice', voice.id)
            tts.runAndWait()

            voice_dir = os.path.join(TTS_BASEDIR, os.path.basename(voice.id))

            # Make directory for TTS output
            if not mkdir(voice_dir):
                continue

            doc_dir = os.path.join(voice_dir, document)
            if not mkdir(doc_dir):
                continue

            ################################ GENERATE WAV FILES ################################
            print_and_say(f"{current_speaker()} is reading {document}.")

            for i, (section, lines) in enumerate(sections.items(), start=1):
                sec_dir = os.path.join(doc_dir, slugify(section))
                if not mkdir(sec_dir):
                    continue

                print_and_say(f"{i}.\t{section}")
                matches = re.finditer(freenode_OnlineCop_re, "\n".join(lines))
                for n, match in enumerate(matches, start=1):
                    prefix, title, punctuation, body = match.groups()
                    line = match.group(0)
                    logging.debug(n, prefix, title)
                    wav_out = os.path.join(sec_dir, f'{n}-{slugify(title)}.wav')
                    if not os.path.exists(wav_out):
                        tts.save_to_file(line, wav_out)
                        tts.runAndWait()
    else:
        if indexer:
            # Write Whoosh index
            indexer.commit()

    ################################ QUERY ################################

    while True:
        q = query()
        if not q or q is True:
            continue
        elif q.lower() in 'Qq':
            break

        with ix.searcher() as searcher:
            parser = QueryParser("content", ix.schema).parse(q)
            results = searcher.search(parser)
            # results.fragmenter = highlight.PinpointFragmenter(surround=64, autotrim=True)
            results.fragmenter = highlight.ContextFragmenter(surround=128)
            results.formatter = highlight.UppercaseFormatter()

            if results:
                print_and_say(f"{len(results)} hits for: {q}.")

                grouped_results = dict()
                for result in results:
                    grouped_results.setdefault((result.get('document')),
                                               dict()).setdefault(result.get('section'),
                                                                  list()).append(result)

                for j, (document, sections) in enumerate(grouped_results.items(), start=1):
                    print_and_say(f"Document {j}. {document}")

                    for k, (section, results) in enumerate(sections.items(), start=1):
                        if section.lower() in ['toc', 'table of contents']:
                            continue

                        print_and_say(section, print_prefix=f"\t{j}\tSection {k}.\t")

                        for result in sorted(results, key=lambda result: result.get('line')):
                            highlights = result.highlights("content")

                            for line in highlights.split("\n"):
                                if line:
                                    print_and_say(f"\t\t\t{line}")
            else:
                print_and_say(f"No hits for {q}.")


if __name__ == '__main__':
    main()
