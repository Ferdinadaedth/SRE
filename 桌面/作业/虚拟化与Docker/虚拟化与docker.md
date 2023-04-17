# Level1

```
systemtcl start docker
docker pull nginx
docker images
docker run -d nginx 
docker ps
docker exec -it 7f961555b0f1 bash
mkdir index.html
echo "I am ironman" > /usr/share/nginx/html/index.html
exit
docker commit nginx mynginx 
```

# Level2

```
systemtcl start docker
vim a.txt 
小黑子一树枝666
mkdir buildfile && cd buildfile
cat a.txt > index.html
FROM nginx
WORKDIR /app
COPY . .
RUN cat a.txt > /usr/share/nginx/html/index.html
docker build -t mynginx:v2 .
docker login
docker tag mynginx:v2 ferdina/mynginx:v2
docker push ferdina/mynginx:v2
docker run  -d -p 8080:80 ferdina/mynginx:v2
curl localhost:8080
小黑子一树枝666
```

[镜像地址](https://hub.docker.com/repository/docker/ferdina/mynginx)

