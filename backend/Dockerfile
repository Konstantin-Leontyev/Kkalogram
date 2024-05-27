FROM python:3.9

RUN apt-get update && \
    apt-get -y install -f && \
    apt-get -y full-upgrade && \
    apt-get -y autoremove && \
    apt-get -y autoclean && \
    apt-get -y clean && \
    apt-get install -y libpq-dev gcc netcat-traditional

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]