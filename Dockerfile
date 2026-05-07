# ---- builder ----
FROM python:3.13.9-alpine3.22 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code 

RUN apk add --no-cache git

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ---- runner ----
FROM python:3.13.9-alpine3.22 AS runner 
COPY src/ .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup botuser

COPY --from=builder /install /usr/local
COPY src/ .

USER botuser

CMD ["python","-u","./main.py"]

