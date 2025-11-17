FROM python:3.12.12-alpine3.22
LABEL maintainer="bokovdenys.dev@gmail.com"
ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /files/media
RUN mkdir -p /files/static

RUN adduser \
    --disabled-password \
    --no-create-home \
    app_user

RUN chown -R app_user /files/media /files/static
RUN chmod -R 755 /files/media /files/static

USER app_user
