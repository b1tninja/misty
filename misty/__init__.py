import logging
import random
import re

import nltk
import pyttsx3
from nltk.corpus import stopwords

nltk.download('stopwords')

voice_re = re.compile(
    r"(?P<vendor>Microsoft) (?P<name>\w+)(?:\s(?P<platform>\w+))? - (?P<lang>\w+)(?:\s*\((?P<region>[^)]+)\))?")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tts = pyttsx3.init()

voices = tts.getProperty('voices')
random.shuffle(voices)
voices = dict([(voice.id, voice) for voice in voices if 'english' in voice.name.lower()])
voice_desc = dict([(voice.id, voice_re.match(voice.name).groupdict()) for voice in voices.values()])
en_stopwords = stopwords.words('english')
