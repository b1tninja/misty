# TODO multiprocessing
import os.path
import string
from collections import OrderedDict
from contextlib import closing
from itertools import cycle

import bcolors

from . import voices, tts, voice_desc, logger

# TODO googletrans
# from googletrans import Translator
# translator = Translator()

voice_iter = cycle(voices.keys())


def current_voice():
    voice_id = tts.getProperty('voice')
    return voices.get(voice_id)


def current_speaker():
    voice_id = tts.getProperty('voice')
    return voice_desc.get(voice_id).get('name')

def print_and_say(text, print_prefix=None, print_suffix=None, next_voice=False):
    print(f"{bcolors.ITALIC}{current_speaker():>12}{bcolors.END}:\t{print_prefix or ''}{text}{print_suffix or ''}")
    tts.say(text)

    if next_voice:
        tts.setProperty('voice', next(voice_iter))

    tts.runAndWait()


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info(f"Creating {os.path.basename(path)} folder.")
        return True
    else:
        assert os.path.isdir(path)
        return False


def slugify(s, maxlen=32):
    filename_sane = set(string.ascii_letters + string.digits + '.-_ ')
    return "".join(x for x in s if x in filename_sane)[:maxlen]


def read_lines(path):
    with closing(open(path, 'r', encoding='utf8')) as fh:
        for line in map(str.strip, iter(fh.readline, '')):
            if line == '________________':
                continue
            yield line


def get_sections(path):
    # _{16}\n*(^[A-z].*?$)\n
    # Iterate over lines, capturing prefixes and "titles".
    txt_file = open(path, 'r', encoding='utf-8-sig')
    sections = OrderedDict()
    previous_line = page = None
    for line in txt_file:
        text = line.strip()
        if not text:
            continue
        # TODO: cleanup with next()
        if text == '________________':
            page = None
        else:
            if page is None:
                page = text
                continue
            sections.setdefault(page, list()).append(text)
            previous_line = text
    return sections


import random


def query():
    speaker = current_speaker()
    prompts = ['What shall I search for?',
               'Your command is my wish.',
               'State your query.',
               f'Hello, I am {speaker}. What am I looking for?',
               f"{speaker} at your service.",
               f"Tell me, what am I seeking? Shall I destroy it?",
               "Protovision, I have you now.",
               "Hello? Saul's fish market.",
               "Shall we play a game?"]

    phrase = cycle(prompts)
    prompt = random.choice(prompts)
    print_and_say(prompt)
    try:
        q = input('> ')
    except EOFError:
        pass
    else:
        if not q:
            print_and_say("Let me get someone else to assist you.", next_voice=True)
            return False

    if prompt == prompts[-1] and ord(q[0]) in [121, 89]:
        print_and_say(f"GREETINGS PROFESSOR FALKEN.")
        for x in range(10, -1, -1):
            print_and_say(f"{x}")
        else:
            print_and_say("CPE 1704 TKS")
            print_and_say("HE'S GOT THE CODE!")
            import time
            time.sleep(5)
            print_and_say(f"Crystal Palace are you still there?")
            input()
            print_and_say("A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.")
            return True

    return q
