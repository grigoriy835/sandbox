Commands to setup or update app 
copy folder to your server and go into that folder
you need add config from crontab file to your /etc/crontab
then do next commands

docker build -t fetch_cars .

docker rm fetch_cars

docker run -d --name fetch_cars --restart no -v $(pwd)/old_records.json:/app/old_records.json fetch_cars

