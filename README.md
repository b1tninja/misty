# misty
Mystical Communal Promulgations... mulgare! Capitulate! Lactate! Promulgate!

## YouTube Demos
- [misty](https://youtu.be/GPdXXqWufwQ) - text to speech helper Ms. Ty
- [query](https://youtu.be/r_sMrRFOs9o) - whoosh full-text searching of Tesseract-OCR'd PDFs/TXTs/JPGs
- [definitions.py](https://youtu.be/p3cHpwhZEfo) - Synonyms, Antonyms, Definitions, See: recursive
- [ud.py](https://youtu.be/Rjo20dU0LGA) - UrbanDictionary
- [ca.py](https://youtu.be/KEum-wb0A1M) - California Code Reader (pubinfo_*.zip dat/lob parser)
- [sacrec.py](https://youtu.be/Y1Bex2CdNx0) - Sacramento County Clerk Recorder Index Synchronizer

## California Codes

`ca.py` is a California codes reader, capable of full text search and plain text printing of the [pubinfo_2021.zip](https://downloads.leginfo.legislature.ca.gov/pubinfo_2021.zip).

The plain-text capabilities come from [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) 's [html2text](https://pypi.org/project/html2text/) library.

Read more about the legislatures "pubinfo" format [here](https://downloads.leginfo.legislature.ca.gov/pubinfo_Readme.pdf), and my opinions about edicts of government on leginfo [feedback page](https://leginfo.legislature.ca.gov/faces/feedbackDetail.xhtml?primaryFeedbackId=prim1614216471200).

```shell
wget -r -c -np -l 1 -A zip downloads.leginfo.legislature.ca.gov
python3 ca.py
```

# Setup
Check out from Github
```shell
git clone https://github.com/b1tninja/misty --single-branch --depth 1
```

### Ubuntu
```shell
sudo apt update
sudo apt install python3-pip
```

### virtualenv for python (optional)
Unfamiliar with Python Virtual Environments? Read the [venv](https://docs.python.org/3/tutorial/venv.html) docs.

#### Install virtualenv for python3
```shell
sudo apt install python3-virtualenv
```
or (but not both) 
```shell
sudo pip3 --install virtualenv
```

#### Create a new virtualenv
virtualenvs are sort of user copies of a python environment to install the optional dependencies in.
```shell
cd misty
python3 -m virtualenv venv
```

#### Activate the "virtualenv"
This changes which python/pip binaries are used, so you don't need to modify your (whole-)system python environment
```shell
. venv/bin/activate
```
### Install optional dependencies
Using requirements.txt
```shell
pip3 install -r requirements.txt
```
or pick and choose
```shell
pip3 install html2text
pip3 install tqdm
```
