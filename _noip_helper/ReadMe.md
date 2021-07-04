docker build -t noip .

docker run -p 7777:7777 -d --name noip --restart unless-stopped noip 7777