simple server for tests


docker build -t RAT .

docker run -p 9890:9890 -d --name RAT --restart unless-stopped RAT