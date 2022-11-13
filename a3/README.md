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
