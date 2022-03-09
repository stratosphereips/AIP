# Docker image for AIP

### Build the image
To build the image, you can run the following command.
```
docker build --file etc/docker/Dockerfile --tag $IMAGE_NAME:$IMAGE_TAG .
```

### Run the container
To run the container of that image you can run the following command. This will mount the root folder of the project in $HOME/AIP inside the docker container.
```
docker run -v $(pwd):/home/aip-ng/AIP/:rw -it aip:aip bash
```

### Run the tests
Once inside the container you need to activate the conda aip environment in order to be able to run the tests.
```
(base) aip-ng@a2aa875c07cf:~/AIP$ conda activate aip
(aip) aip-ng@a2aa875c07cf:~/AIP$ pytest tests/
```

