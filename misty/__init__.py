import logging
import re

import pyttsx3

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

voice_re = re.compile(r"(?P<vendor>Microsoft) (?P<name>\w+)(?:\s(?P<platform>\w+))? - (?P<lang>\w+) (?P<region>[^)]+)")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tts = pyttsx3.init()

voices = dict([(voice.id, voice) for voice in tts.getProperty('voices')])
voice_desc = dict([(voice.id, voice_re.match(voice.name).groupdict()) for voice in voices.values()])
en_stopwords = stopwords.words('english')