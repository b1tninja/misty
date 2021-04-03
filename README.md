# misty
Mystique Community Association python musings

Unfamiliar with Python Virtual Environments? Read the [venv](https://docs.python.org/3/tutorial/venv.html) docs.

## YouTube Demos
- [misty](https://youtu.be/GPdXXqWufwQ)
- [query](https://youtu.be/r_sMrRFOs9o)
- [definitions.py](https://youtu.be/p3cHpwhZEfo)
- [ud.py](https://youtu.be/Rjo20dU0LGA)
- [ca.py](https://youtu.be/KEum-wb0A1M)

## California Codes

`ca.py` is a California codes reader, capable of full text search and plain text printing of the [pubinfo_2021.zip](https://downloads.leginfo.legislature.ca.gov/pubinfo_2021.zip).

The plain-text capabilities come from Aaron Swartz's html2text library.

Read more about the legislatures "pubinfo" format [here](https://downloads.leginfo.legislature.ca.gov/pubinfo_Readme.pdf).

```shell
wget -r -c -np -l 1 -A zip downloads.leginfo.legislature.ca.gov
python3 ca.py
```
