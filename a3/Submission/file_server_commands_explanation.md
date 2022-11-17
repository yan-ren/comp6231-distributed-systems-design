## File server commands explanation

#### File server
1. Create file_server_server_DockerFile with following content. This file is used to build file server image.
```docker
# declare base image
FROM python:3.8

ENV WORK_DIR=/home/server
# set work directory
RUN mkdir -p $WORK_DIR
# where server code lives
WORKDIR $WORK_DIR

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy server project code
COPY server $WORK_DIR/
COPY server.py $WORK_DIR

# expose the port
EXPOSE 65432

# go to work directory and start the server.py
RUN cd $WORK_DIR
CMD ["python", "server.py"]
```
2. Build server image using `file_server_server_DockerFile`
```
docker build -t server -f file_server_server_DockerFile .
```

3. Run server container
```
docker run -d -p 65432:65432 server
```

#### File Client

1. Create file_server_client_DockerFile with following content. This file is used to build file client image.
```docker
FROM python:3.8

ENV WORK_DIR=/home/client
# set work directory
RUN mkdir -p $WORK_DIR
# where client code lives
WORKDIR $WORK_DIR

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy client project
COPY client.py $WORK_DIR

EXPOSE 65432

# go to work directory and start the client.py
RUN cd $WORK_DIR
CMD ["python", "client.py"]
```

2. Build client image
```
docker build -t client -f file_server_client_DockerFile .
```

3. Run client container in interative mode, open 3 ternimal windows to create 3 client containers
```
docker run -i --net=host client
docker run -i --net=host client
docker run -i --net=host client
```

4. Client successfully connects to Server
- Server log

![](Screen%20Shot%202022-11-14%20at%201.25.45%20AM.png)
- Client log

![](Screen%20Shot%202022-11-14%20at%201.26.05%20AM.png)

5. List all containers and ip

![](Screen%20Shot%202022-11-14%20at%201.44.53%20AM.png)
