FROM python:3

ADD music-scraper.py /
ADD requirements.txt /


RUN pip3 install -r requirements.txt

CMD [ "python3", "./music-scraper.py" ]