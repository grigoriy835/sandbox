docker build -t fetch_cars .

mkdir logs

docker run -d --name fetch_cars --restart unless-stopped -v ./logs:/logs fetch_cars