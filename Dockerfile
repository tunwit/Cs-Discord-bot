FROM python:3.11.10-alpine3.20
WORKDIR /code 
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY src/ .
CMD ["python","-u","./main.py"]

