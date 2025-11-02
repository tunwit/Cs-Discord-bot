FROM python:3.13.9-alpine3.22
WORKDIR /code 
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY src/ .
CMD ["python","-u","./main.py"]

