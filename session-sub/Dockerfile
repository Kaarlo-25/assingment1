FROM python:3.9

WORKDIR /app

COPY session-pub.py .

RUN pip install pika

CMD ["python", "-u", "session-pub.py"]