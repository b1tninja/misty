# misty
Mystique Community Association python musings

## YouTube Demos
- [misty](https://youtu.be/GPdXXqWufwQ)
- [query](https://youtu.be/r_sMrRFOs9o)
- [definitions.py](https://youtu.be/p3cHpwhZEfo)
- [ud.py](https://youtu.be/Rjo20dU0LGA)
- [ca.py](https://youtu.be/KEum-wb0A1M)
- [sacrec.py](https://youtu.be/Y1Bex2CdNx0)

## California Codes

`ca.py` is a California codes reader, capable of full text search and plain text printing of the [pubinfo_2021.zip](https://downloads.leginfo.legislature.ca.gov/pubinfo_2021.zip).

The plain-text capabilities come from Aaron Swartz's [html2text](https://pypi.org/project/html2text/) library.

Read more about the legislatures "pubinfo" format [here](https://downloads.leginfo.legislature.ca.gov/pubinfo_Readme.pdf).

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
