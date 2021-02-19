from itertools import cycle

import logging
import pyttsx3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


tts = pyttsx3.init()
voices = tts.getProperty('voices')
