FROM python:3.9

WORKDIR /app

COPY session-processor.py .

RUN pip install pika pymongo

CMD ["python", "-u", "session-processor.py"]