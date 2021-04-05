FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2021.zip downloads.leginfo.legislature.ca.gov/
ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2019.zip downloads.leginfo.legislature.ca.gov/
ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2017.zip downloads.leginfo.legislature.ca.gov/
ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2015.zip downloads.leginfo.legislature.ca.gov/
ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2013.zip downloads.leginfo.legislature.ca.gov/
ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2011.zip downloads.leginfo.legislature.ca.gov/

# RUN python ./misty/ca.py --json
CMD [ "python", "./misty/ca.py" ]