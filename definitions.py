from collections import deque
from itertools import cycle

import bcolors
import pyttsx3
from PyDictionary import PyDictionary

from misty import en_stopwords, logger
from misty.utils import print_and_say

dictionary = PyDictionary()
tts = pyttsx3.init()
voices = cycle(tts.getProperty('voices'))
unknown_words = set()


def lookup(word):
    print_and_say(word, print_prefix=bcolors.UNDERLINE + bcolors.BOLD, print_suffix=bcolors.END)
    yield from read_definitions(word)
    yield from read_synonyms(word)
    yield from read_antonyms(word)


def read_synonyms(word):
    synonyms = dictionary.synonym(word)
    if synonyms is None:
        print_and_say(f"No synonyms known for {word}.")
    else:
        print_and_say(f"Found {len(synonyms)}  synonyms for {word}.")
        for n, synonym in enumerate(synonyms):
            print_and_say(f"\t{n + 1}.\t {synonym}.")
            yield synonym


def read_antonyms(word):
    antonyms = dictionary.antonym(word)
    if antonyms is None:
        print_and_say(f"No antonyms known for {word}.")
    else:
        print_and_say(f"Found {len(antonyms)}  antonyms for {word}.")
        for n, antonym in enumerate(antonyms):
            print_and_say(f"\t{n + 1}.\t {antonym}.")
            yield antonym


def read_definitions(word):
    definition = dictionary.meaning(word)
    if definition is None:
        print_and_say(f"The definition for {word} is unknown.")
        unknown_words.add(word)
    else:
        for part_of_speech, meanings in definition.items():
            print_and_say(f"{word}, the {part_of_speech}, has {len(meanings)} meanings.")
            for n, meaning in enumerate(meanings):
                print_and_say(f"\t{n + 1}.\t{meaning}")
                for related_word in meaning.split(" "):
                    yield related_word


if __name__ == '__main__':
    # pending = deque(['capitulate', 'whimsical'])
    # pending = deque(['axiomatic', 'disdain'])
    pending = deque(['attrition'])

    while pending:
        try:
            word = pending.popleft()
        except IndexError:
            continue
        else:
            for related_entry in lookup(word):
                if related_entry not in en_stopwords:
                    pending.append(related_entry)
                else:
                    logger.debug(f"Skipping {related_entry}...", print_prefix=bcolors.WARN, print_suffix=bcolors.END)
