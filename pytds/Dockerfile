FROM python:3

RUN apt-get update
RUN apt-get install -y vim netcat mc git htop

RUN mkdir /usr/share/GeoIP
COPY GeoIP.dat /usr/share/GeoIP/GeoIP.dat
COPY GeoIPv6.dat /usr/share/GeoIP/GeoIPv6.dat

copy ssh /root/.ssh
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

RUN echo "lol2"
RUN git clone git@bitbucket.org:oneclickflow/pytds.git /pytds
WORKDIR /pytds

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["sh", "-c", "gunicorn server:app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker --workers 50 --keep-alive 10"]