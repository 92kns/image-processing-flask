# from alpine:latest
#  slim buster is better apparently
from python:3.8-slim-buster
# testing new
ADD . /app
WORKDIR /app

ENV FLASK_APP=imageserver.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
RUN pip install -r requirements.txt
# RUN ./mybashscript.sh

# old copy
# ENV FLASK_APP=imageserver.py
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=8080


# WORKDIR /app

# COPY requirements.txt /app
# RUN pip install -r /app/requirements.txt

# COPY . /app

# #  default port is 5000 on my local pc
# #  default is 8080 on GCP, let's just use that
# EXPOSE 8080
# ENV PORT 8080

# # no need to have a seperate container for DB for this small app. 
# # hence the docker-compose.yml likewise doesn't have another DB service
# RUN flask init-db

# for debugging/dev server------------
CMD ["flask","run","--host=0.0.0.0"]

# for light weight production server. currently used on GCP---------------
# RUN pip install waitress
# CMD waitress-serve --call 'testapp:create_app'

