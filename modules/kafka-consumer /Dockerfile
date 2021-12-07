FROM python:3.8-buster

WORKDIR .

RUN apt-get install gcc libc-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 50053

COPY . .
CMD ["python", "consumer.py"]