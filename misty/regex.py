import re

# TODO: strip white space and punctuation from body
freenode_OnlineCop_re = re.compile(r"""
^\s*
(?P<leading_number>[0-9.]+|\([a-z0-9A-Z]+\))?
\s*
(?P<title>
  (?:[^\d.;?\n]+
  |
  \d+(?:\.\d+(?:[0-9]+\.)*)?
  )* # Non-digits
)
(?P<punctuation>[.;?,]|$)(?P<body>.*?$)
""", re.MULTILINE | re.VERBOSE)

# _{16}\n*(^[A-z].*?$)\n
# Iterate over lines, capturing prefixes and "titles".
