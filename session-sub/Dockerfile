FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install pika

CMD ["python", "-u", "session_pub.py"]