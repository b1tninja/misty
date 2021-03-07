from itertools import permutations

from misty.utils import print_and_say


def variants(charset):
    for l in range(len(charset), 1, -1):
        for combination in permutations(charset, l):
            yield ''.join(combination)


if __name__ == '__main__':
    variations = variants('saturday')
    skip = next(variations)
    for i, variant in enumerate(variations, start=1):
        print_and_say(''.join(variant), print_prefix=f"{i}.\t", next_voice=True)
