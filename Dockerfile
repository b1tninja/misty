FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ADD https://downloads.leginfo.legislature.ca.gov/pubinfo_2021.zip downloads.leginfo.legislature.ca.gov/

CMD [ "python", "./misty/ca.py" ]