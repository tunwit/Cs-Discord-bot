# ---- builder ----
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code 

RUN apt-get update && apt-get install -y git
    
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ---- runner ----
FROM python:3.13-slim AS runner 

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libopus0

COPY src/ .

RUN addgroup --system appgroup && adduser --system --ingroup appgroup botuser

COPY --from=builder /install /usr/local
COPY src/ .

USER botuser

CMD ["python","-u","./main.py"]

