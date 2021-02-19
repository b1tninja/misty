from collections import deque
from itertools import cycle

import bcolors
import pyttsx3
from PyDictionary import PyDictionary

dictionary = PyDictionary()
tts = pyttsx3.init()
voices = cycle(tts.getProperty('voices'))
unknown_words = set()


def print_and_say(text, print_prefix=None, print_suffix=None):
    print((print_prefix or '') + text + (print_suffix or ''))
    tts.say(text)
    tts.runAndWait()
    tts.setProperty('voice', next(voices).id)


def lookup(word):
    global unknown_words

    print_and_say(word, print_prefix=bcolors.UNDERLINE + bcolors.BOLD, print_suffix=bcolors.END)

    to_lookup = set()

    synonyms = dictionary.synonym(word)
    if synonyms is None:
        print_and_say(f"No synonyms known for {word}.")
    else:
        print_and_say(f"Found {len(synonyms)}  synonyms for {word}.")
        for n, synonym in enumerate(synonyms):
            print_and_say(f"\t{n+1}.\t {synonym}.")
            to_lookup.add(synonym)

    antonyms = dictionary.antonym(word)
    if antonyms is None:
        print_and_say(f"No antonyms known for {word}.")
    else:
        print_and_say(f"Found {len(antonyms)}  antonyms for {word}.")
        for n, antonym in enumerate(antonyms):
            print_and_say(f"\t{n+1}.\t {antonym}.")
            to_lookup.add(antonym)

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
                    to_lookup.add(related_word)

    while to_lookup:
        try:
            yield to_lookup.pop()
        except IndexError:
            continue


if __name__ == '__main__':
    pending = deque(['capitulate', 'whimsical'])

    while pending:
        word = pending.popleft()
        for related_entry in lookup(word):
            # TODO: prune stop words
            pending.append(related_entry)

