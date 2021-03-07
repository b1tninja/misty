import datetime
import logging
from itertools import permutations
from random import sample, randint
from string import ascii_letters

from nltk.corpus import brown

from misty.utils import print_and_say

category = sample(brown.categories(), 3)[0]
category = None

# print_and_say(f"Selected {category} for sub words")

logging.warning("Loading Brown University corpus of words")
words = set(map(str.lower, brown.words(categories=category)))  # nltk.corpus.brown
print_and_say(f'Loaded {len(words)} "{category}" words.')


def variants(charset):
    for l in range(len(charset), 1, -1):
        for combination in permutations(charset, l):
            yield ''.join(combination)


def get_subwords(word):
    logging.info(f"Iterating over permutations of {word}")
    print_and_say(word, next_voice=True)
    variations = variants(word)
    # skip = next(variations)
    for i, variant in enumerate(variations, start=1):
        prefix = f"{i}.\t"
        if variant in words:
            yield variant


def get_subwords_of_phrase(phrase):
    words = phrase.split(' ')
    for word in words:
        yield from get_subwords(word)


if __name__ == '__main__':
    original = "capitulate"  # lactate promulgate
    print_and_say(original)
    parts = [c for c in original.lower() if c in set(ascii_letters + ' ')]
    # shuffle(parts)
    phrase = ''.join(parts)
    start = datetime.datetime.now()
    words = list(get_subwords_of_phrase(' '.join(set(phrase.split(' ')))))
    wc = len(phrase.split(' '))
    while True:
        l = randint(1, wc)
        # l = randint(1, min(max(len(words),12), len(words)))
        combination = sample(words, l)
        reconstruction = ' '.join(combination)

        if reconstruction == phrase:
            break  # Alert wikipedia! TODO: update wikipedia https://en.wikipedia.org/wiki/Infinite_monkey_theorem

        print_and_say(reconstruction, next_voice=True)

    finish = datetime.datetime.now()
    print_and_say(f"{reconstruction} was found in {(finish - start).total_seconds()} seconds", next_voice=True)
