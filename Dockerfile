FROM python:3.13.9-alpine3.22
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /code 

RUN apk add --no-cache git

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ .

RUN adduser -D appuser
USER appuser

CMD ["python","-u","./main.py"]

