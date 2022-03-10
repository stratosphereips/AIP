# Docker image for AIP
AIP docker aims to help in development and deployment of AIP algorithms to newcommers. The code of the repository is mounted and available from inside the docker image. The source of the data and the output folder of AIP is also mounted as a data volume inside the data/ folder to decouple from where this data really is in the host machine, easying the AIP deployment.

### Build the image
To build the image, you can run the following command.
```
docker build --file etc/docker/Dockerfile --tag aip:aip .
```

### Run the container
To run the container of that image you can run the following command. This will mount the root folder of the project in $HOME/AIP inside the docker container.
```
docker run -v $(pwd):/home/aip/AIP/:rw -it aip:aip bash
```

### Run the tests
Once inside the container you need to activate the conda aip environment in order to be able to run the tests.
```
(base) aip-ng@a2aa875c07cf:~/AIP$ conda activate aip
(aip) aip-ng@a2aa875c07cf:~/AIP$ pytest tests/
```

