import logging
import os
import re

import pyttsx3
from whoosh import index, highlight
from whoosh.fields import SchemaClass, TEXT, ID
from whoosh.qparser import QueryParser

from .config import CORPUS_BASEDIR, WHOOSH_INDEX_BASEDIR, TTS_BASEDIR
from .utils import print_and_say, mkdir, slugify, read_lines
from . import voices

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
    title = TEXT(stored=True)
    content = TEXT(stored=True)


if __name__ == '__main__':
    tts = pyttsx3.init()

    indexer = None

    mkdir(CORPUS_BASEDIR)

    if mkdir(WHOOSH_INDEX_BASEDIR):
        # Make Index
        ix = index.create_in(WHOOSH_INDEX_BASEDIR, TxtSchema)
        indexer = ix.writer()
    else:
        assert os.path.isdir(WHOOSH_INDEX_BASEDIR)
        # Read Index
        ix = index.open_dir(WHOOSH_INDEX_BASEDIR)



    for name in os.listdir(CORPUS_BASEDIR):
        title, ext = os.path.splitext(name)

        if ext.lower() != '.txt':
            continue

        path = os.path.join(CORPUS_BASEDIR, name)

        if indexer:
            print_and_say(f'Indexing "{title}".')
            indexer.add_document(title=title, path=path, content="\n".join(read_lines(path)))

        mkdir(TTS_BASEDIR)
        for voice in voices:
            tts.setProperty('voice', voice.id)
            voice_dir = os.path.join(TTS_BASEDIR, os.path.basename(voice.id))

            # Make directory for TTS output
            if not mkdir(voice_dir):
                continue

            target_dir = os.path.join(voice_dir, title)
            if not mkdir(target_dir):
                continue

            ################################ GENERATE WAV FILES ################################
            print_and_say(f"{voice.name} is reading {title}.")
            # Iterate over lines, capturing prefixes and "titles".
            matches = re.finditer(freenode_OnlineCop_re, open(path, 'r', encoding='utf8').read())
            for n, match in enumerate(matches, start=1):
                prefix, title, punctuation, body = match.groups()
                line = match.group(0)
                logging.debug(n, prefix, title)
                tts.save_to_file(line, os.path.join(target_dir, f'{n}-{slugify(title)}.wav'))
                tts.runAndWait()

    else:
        if indexer:
            # Write Whoosh index
            indexer.commit()

    ################################ QUERY ################################
    with ix.searcher() as searcher:
        print_and_say("Please state your query.")
        query = input("query: ")
        parser = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(parser)
        # results.fragmenter = highlight.PinpointFragmenter(surround=64, autotrim=True)
        results.fragmenter = highlight.ContextFragmenter(surround=128)
        results.formatter = highlight.UppercaseFormatter()

        if results:
            print_and_say(f"Found {len(results)} documents matching: {query}.")

            for n, result in enumerate(results):
                print_and_say(f"Document {n + 1}. {result.get('title')}")

                highlights = result.highlights("content")
                for line in highlights.split("\n"):
                    print_and_say(line)
        else:
            print_and_say(f"No hits for {query}.")
