docker build -t RAT .

docker run -p 7777 -d --name RAT --restart unless-stopped RAT