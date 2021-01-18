
from python:3.8-slim-buster

ADD . /app
WORKDIR /app

ENV FLASK_APP=imageserver.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000
ENV PORT 5000


RUN pip install -r requirements.txt

CMD ["flask","run","--host=0.0.0.0"]

# for light weight production server. better used on GCP
# RUN pip install waitress
# CMD waitress-serve --call 'imageserver:create_app'

