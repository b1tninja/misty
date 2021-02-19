import os.path
import string
from contextlib import closing
from itertools import cycle
import bcolors


from . import voices, tts, voice_desc

voice_iter = cycle(voices.keys())

def current_voice():
    voice_id = tts.getProperty('voice')
    return voices.get(voice_id)

def current_speaker():
    voice_id = tts.getProperty('voice')
    return voice_desc.get(voice_id).get('name')

def print_and_say(text, print_prefix=None, print_suffix=None, next_voice=True):
    print(f"{bcolors.ITALIC}{current_speaker():>12}{bcolors.END}:\t{print_prefix or ''}{text}{print_suffix or ''}")
    tts.say(text)

    if next_voice:
        tts.setProperty('voice', next(voice_iter))

    tts.runAndWait()


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print_and_say(f"Creating {os.path.basename(path)} folder.")
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
