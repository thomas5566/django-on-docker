# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .

# install dependencies
RUN apk update \
     && apk add postgresql-dev \
                gcc \
                python3-dev \
                musl-dev \
                postgresql-client \
                libffi-dev \
                libxml2-dev \
                libxslt-dev \
                python3-dev \
                gcc \
                build-base \
                jpeg-dev \
                zlib-dev \
                freetype-dev \
                lcms2-dev \
                openjpeg-dev \
                tiff-dev \
                tk-dev \
                tcl-dev \
                harfbuzz-dev \
                fribidi-dev

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
&& apk add --update --no-cache py3-numpy py3-pandas@community

# take /requirements.txt installs it using pip into the Docker image
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]