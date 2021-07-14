FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD . /app
WORKDIR /app

EXPOSE 9890

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "response_after_time.py"]