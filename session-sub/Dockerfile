FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install pika

CMD ["python", "session_pub.py"]