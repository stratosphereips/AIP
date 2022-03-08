# Docker image for AIP

To build the image, you can run the following command.
```
docker build --file etc/docker/Dockerfile --tag $IMAGE_NAME:$IMAGE_TAG .
```


To run the container of that image you can run the following command. This will mount the root folder of the project in $HOME/AIP inside the docker container.

```
docker run --rm --volume ${pwd}:/home/aip-ng/AIP/ -it $IMAGE_NAME:$IMAGE_TAG
docker run -v $(pwd):/home/aip-ng/AIP/:rw -it aip:aip bash /usr/local/bin/entrypoint.sh
```
