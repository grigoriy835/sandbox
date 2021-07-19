FROM python:3.9

RUN apt update && apt install -y libxml2 libxslt
RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "fetch_cars.py"]