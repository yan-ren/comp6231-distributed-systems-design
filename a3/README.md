## Task 1

#### Build server image
```
docker build -t server -f file_server_server_DockerFile .
```

#### Run server container
```
docker run -d -p 65432:65432 server
```


#### Build client image
```
docker build -t client -f file_server_client_DockerFile .
```

#### Run client container
```
docker run -i --net=host client
```

#### Access client container to verify the download
```
docker exec -it <mycontainer> bash
```

```
docker run -dit husseinabdallah2/mpi4py-cluster:master

list containers ips
(docker ps -q | ForEach-Object { docker inspect $_ --format '{{ .NetworkSettings.IPAddress }} {{ .Name }}' }).replace('/','')

172.17.0.5 elegant_kapitsa
172.17.0.4 heuristic_golick
172.17.0.3 pensive_jemison
172.17.0.2 crazy_ride

ssh-copy-id -i ~/.ssh/id_rsa.pub root@172.17.0.3


docker cp . crazy_ride:/root/
docker cp . pensive_jemison:/root/
docker cp . heuristic_golick:/root/
docker cp . elegant_kapitsa:/root/
```
