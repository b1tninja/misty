from collections import deque
import urbandict

from misty import en_stopwords
from misty.utils import print_and_say


def lookup(word):
    print_and_say(word)

    for definition in urbandict.define(word):
        print_and_say(f"Definition: {definition['def']}", print_prefix="\t")
        for related_entry in filter(lambda rw: rw not in en_stopwords, definition['def'].split()):
            yield related_entry

        print_and_say(f"For example: {definition['example']}", print_prefix="\t")
        for related_entry in filter(lambda rw: rw not in en_stopwords, definition['example'].split()):
            yield related_entry

if __name__ == '__main__':
    pending = deque(['Chad'])

    while pending:
        try:
            word = pending.popleft()
        except IndexError:
            continue
        else:
            for related_entry in lookup(word):
                pending.append(related_entry)
