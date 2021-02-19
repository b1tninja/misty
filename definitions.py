from itertools import cycle

import bcolors
import pyttsx3
from PyDictionary import PyDictionary

dictionary = PyDictionary()
tts = pyttsx3.init()
word = 'recursive'
looked_up = set()  # TODO: FIFO?
voices = cycle(tts.getProperty('voices'))
unknown_words = set()


def print_and_say(text, print_prefix=None, print_suffix=None):
    print((print_prefix or '') + text + (print_suffix or ''))
    tts.say(text)
    tts.runAndWait()
    tts.setProperty('voice', next(voices).id)


def lookup(word, depth=0):
    global looked_up
    global unknown_words

    print_and_say(word, print_prefix=bcolors.UNDERLINE + bcolors.BOLD, print_suffix=bcolors.END)

    to_lookup = set()
    looked_up.add(word)

    synonyms = dictionary.synonym(word)
    if synonyms is None:
        print_and_say(f"No synonyms known for {word}.")
    else:
        print_and_say(f"The following {len(synonyms)} words are synonyms of {word}.")
        for n, synonym in enumerate(synonyms):
            print_and_say(f"{synonym}", print_prefix=f"\t{n}.\t", print_suffix=".")
            to_lookup.add(synonym)

    antonyms = dictionary.antonym(word)
    if antonyms is None:
        print_and_say(f"No antonyms known for {word}.")
    else:
        print_and_say(f"The following {len(antonyms)} words are antonyms of {word}.")
        for n, antonym in enumerate(antonyms):
            print_and_say(f"{antonym}", print_prefix=f"\t{n}.\t", print_suffix=".")
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
                    if related_word not in looked_up:
                        to_lookup.add(related_word)

    while to_lookup:
        print(f"{word} - {len(looked_up)} defined, {len(to_lookup)} pending.")
        try:
            lookup(to_lookup.pop(), depth + 1)
        except IndexError:
            break

try:
    lookup(word)
except:
    pass
finally:
    print(unknown_words)
    print(looked_up)
