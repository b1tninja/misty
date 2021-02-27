# TODO multiprocessing
import os
import os.path
import random
import string
from collections import OrderedDict
from contextlib import closing
from itertools import cycle

import bcolors

from . import voices, tts, voice_desc, logger, en_stopwords
# TODO googletrans
# from googletrans import Translator
# translator = Translator()
from .config import DEFAULT_ENCODING

voice_iter = cycle(voices.keys())


def filter_stopwords(words):
    return filter(lambda word: word not in en_stopwords, words)


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


def read_lines(path, strip_empty_lines=True):
    with closing(open(path, 'r', encoding='utf-8-sig')) as fh:
        for line in iter(fh.readline, ''):
            if line.strip():
                yield line.rstrip()


def get_sections(path, skip=None):
    assert type(skip) in [list, str]

    sections = OrderedDict()
    page = os.path.splitext(os.path.basename(path))[0]
    lines = iter(read_lines(path))

    while True:
        try:
            line = next(lines)
            # text = line.strip()
            if line == '________________':
                page = next(lines).strip()
                continue
            else:
                if type(skip) is list and page in skip:
                    continue
                elif type(skip) is str and page == skip:
                    continue
                sections.setdefault(page, list()).append(line)
        except StopIteration:
            break

    return sections


def query():
    speaker = current_speaker()
    # TODO: change to format
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


def parse_document(path, **meta_data):
    d = dict(meta_data)
    d.setdefault('path', path)
    d.setdefault('name', os.path.splitext(os.path.basename(path))[0])
    d.update(sections=get_sections(path, ['TABLE OF CONTENTS']))
    return d


# TODO: fridge detective tangent?
def for_file_path_name_by_ext(basedir, ext):
    if type(ext) is list:
        ext = list(map(str.lower, ext))

    for path, name, file_name, file_ext in for_file_path_name_ext_in(basedir):
        assert type(ext) in [list, str]
        if type(ext) is str and file_ext.lower() != ext.lower():
            continue

        elif type(ext) is list and file_ext not in ext:
            continue

        yield path, name, file_name, file_ext


def for_path_name_is_file_in(basedir):
    for name in os.listdir(basedir):
        path = os.path.join(basedir, name)
        is_file = os.path.isfile(path)
        yield path, name, is_file


def for_file_path_name_ext_in(basedir):
    for path, name, is_file in for_path_name_is_file_in(basedir):
        if not is_file:
            continue

        file_name, ext = os.path.splitext(name)

        assert ext[0] == '.'
        yield path, name, file_name, ext[1:].lower()


def save_txt(path, text):
    with closing(open(path, 'w', encoding=DEFAULT_ENCODING)) as fh:
        fh.write(text)
