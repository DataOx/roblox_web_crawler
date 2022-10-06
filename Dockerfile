FROM python:3.8.10-slim-buster as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

RUN useradd crawlercelery
RUN chown -R crawlercelery:crawlercelery /app
RUN chmod +x /app/web-runner.sh
