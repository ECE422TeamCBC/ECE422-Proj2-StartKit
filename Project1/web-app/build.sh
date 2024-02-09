docker build -t server-app .
docker tag server-app:latest carlhat/server-app:latest
docker push carlhat/server-app:latest