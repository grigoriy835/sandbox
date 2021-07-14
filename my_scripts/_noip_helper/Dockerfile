FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "noip_helper.py"]