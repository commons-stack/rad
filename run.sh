#!/bin/bash  

IMAGE=$( docker images | grep rad )
if [ -z "$IMAGE" ]
then
  echo "Building image..."
  docker build --tag rad .
else
  echo "Using built image."
fi

CONTAINER=$( docker ps | grep rad | cut -d' ' -f1 )
if [ -z "$CONTAINER" ]
then
  echo "Starting container..."
  docker run --rm -d -it -v $(pwd):/app rad sleep infinity
else
  echo "Container is running."
fi

docker exec -ti $( docker ps | grep rad | cut -d' ' -f1 ) bash