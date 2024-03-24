FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# --no-cache: Do not store the registry index on our docker file
# because we want to minimize the number of extra files and packages that
# are included in our docker container.
RUN apk add --update --no-cache postgresql-client

# --virtual: Packages added under this virtual name can then be removed as one group.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# # This would be removing a group of build dependencies all at once.
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D --disabled-password  Don't assign a password, so cannot login
RUN adduser -D user
USER user
