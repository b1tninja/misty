import datetime
import logging
from itertools import permutations
from random import sample, randint

from nltk.corpus import brown

from misty.utils import print_and_say

category = sample(brown.categories(), 3)[0]

print_and_say(f"Selected {category} for sub words")

logging.warning("Loading Brown University corpus of words")
words = set(map(str.lower, brown.words(categories=category)))  # nltk.corpus.brown
print_and_say(f'Loaded {len(words)} "{category}" words.')


def variants(charset):
    for l in range(len(charset), 1, -1):
        for combination in permutations(charset, l):
            yield ''.join(combination)


def get_subwords(word):
    logging.info(f"Iterating over permutations of {word}")
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
    phrase = 'Whether tis nobler in the mind to suffer'.lower()
    start = datetime.datetime.now()
    words = list(get_subwords_of_phrase(phrase))
    while True:
        l = randint(1, len(phrase.split(' ')))
        combination = sample(words, l)
        reconstruction = ' '.join(combination)

        if reconstruction == phrase:
            break

        print_and_say(reconstruction, next_voice=True)

    finish = datetime.datetime.now()
    print_and_say(f"{reconstruction} was found in {finish - start}", next_voice=True)

# if __name__ == '__main__':
#     words = list(get_subwords_of_phrase(phrase))
#     shuffle(words)
#     # for l in range(len(phrase.split(' ')):
#     l = len(phrase.split(' '))
#     for i, combination in enumerate(combinations(words, l), start=1):
#         combination = list(combination)
#         shuffle(combination)
#         print_and_say(' '.join(combination), print_prefix=f"{i}.\t", next_voice=True)
#
#
# if __name__ == '__main__':
#     words = set(get_subwords(''))
#     for l in range(len(words)):
#         combs = list(combinations(words, l))
#         shuffle(combs)
#         for i, combination in enumerate(combs, start=1):
#             print_and_say(' '.join(combination), print_prefix=f"{i}.\t", next_voice=True)
