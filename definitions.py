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

import string
def lookup(word):
    word = "".join(x for x in word if x in set(string.ascii_letters))
    print_and_say(word, print_prefix=bcolors.UNDERLINE + bcolors.BOLD, print_suffix=bcolors.END)
    yield from read_synonyms(word)
    yield from read_antonyms(word)
    yield from read_definitions(word)


def read_synonyms(word):
    synonyms = dictionary.synonym(word)
    if synonyms is None:
        print_and_say(f"No synonyms known for {word}.")
    else:
        print_and_say(f"Found {len(synonyms)}  synonyms for {word}.")
        for n, synonym in enumerate(synonyms):
            print_and_say(synonym, print_prefix=f"\t{n + 1}.\t", print_suffix='.')
            yield synonym


def read_antonyms(word):
    antonyms = dictionary.antonym(word)
    if antonyms is None:
        print_and_say(f"No antonyms known for {word}.")
    else:
        print_and_say(f"Found {len(antonyms)}  antonyms for {word}.")
        for n, antonym in enumerate(antonyms):
            print_and_say(antonym, print_prefix=f"\t{n + 1}.\t")
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
    pending = deque(['keeper'])

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
