service to host services from home with dynamic ip by running this service on a host with static ip


docker build -t noip .

docker run -p 7777:7777 -d --name noip --restart unless-stopped noip 7777