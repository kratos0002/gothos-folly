FROM python:3

ADD quotes-scraper.py /
ADD requirements.txt /


RUN pip3 install -r requirements.txt

CMD [ "python3", "./quotes-scraper.py" ]