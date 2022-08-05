service for crawling adverb site with cars and notify about fresh lots


Commands to setup or update app 

- you need add config from crontab file to your /etc/crontab
- copy app folder to your server and go into that folder

- then do next commands

``docker build -t fetch_cars .``

``docker rm fetch_cars``

``docker run -d --name fetch_cars --restart no -v $(pwd)/old_records.json:/app/old_records.json -v $(pwd)/proxy_list.json:/app/proxy_list.json -v $(pwd)/sources.json:/app/sources.json fetch_cars fetch_cars.py``

