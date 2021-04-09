import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    import nltk
except (ImportError, ModuleNotFoundError):
    logging.warning("nltk library provides stop words and categories for words")
else:
    from nltk.corpus import stopwords

    nltk.download('stopwords')
    en_stopwords = stopwords.words('english')

try:
    import pyttsx3
except (ImportError, ModuleNotFoundError):
    logging.warning("pyttsx3 offers Microsoft text-to-speech support")
else:
    tts = pyttsx3.init()

    voices = tts.getProperty('voices')
    voice_re = re.compile(r"(?P<vendor>Microsoft) (?P<name>\w+)(?:\s(?P<platform>\w+))? - (?P<lang>\w+)(?:\s*\((?P<region>[^)]+)\))?")
    voices = dict([(voice.id, voice) for voice in voices if 'english' in voice.name.lower()])
    voice_desc = dict([(voice.id, voice_re.match(voice.name).groupdict()) for voice in voices.values()])
