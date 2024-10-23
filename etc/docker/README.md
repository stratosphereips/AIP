# Docker image for AIP

AIP docker aims to help in development and deployment of AIP algorithms to newcommers. The code of the repository is mounted and available from inside the docker image. The source of the data and the output folder of AIP is also mounted as a data volume inside the data/ folder to decouple from where this data really is in the host machine, easying the AIP deployment.

## Build the image

To build the image, you can run the following command.

```bash
:~$ git clone https://github.com/stratosphereips/AIP.git
:~$ cd AIP/
:~/AIP$ docker build --build-arg uid=1000 --file etc/docker/Dockerfile --tag aip:latest .
```

## Prepare the data

AIP needs raw network flow data to run. In this case, we assume you have Zeek logs in `/opt/zeek/logs`. 

Additionally, the following two files need to be edited and populated:
- `data/external/do_not_block_these_ips_example.csv`: you want to add here IPs that should not appear on the AIP blocklists
- `data/external/honeypots_public_ips_example.csv`: you want to add here the public IP of the honeypot or machine running Zeek

First copy the files and then edit them:
```bash
:~/AIP$ cp data/external/do_not_block_these_ips_example.csv data/external/do_not_block_these_ips.csv
:~/AIP$ cp data/external/honeypots_public_ips_example.csv data/external/honeypots_public_ips.csv
```

## Run the container

To run the container of that image you can run the following command:

```bash
:~/AIP$ docker run --rm -v /opt/zeek/logs/:/home/aip/AIP/data/raw:ro -v ${PWD}/data/:/home/aip/AIP/data/:rw --name aip aip:latest bin/aip
```

An example output is shown below:
```
2024-10-23 13:02:36,513 - aip.data.access - DEBUG - Creating attacks for dates ['2024-10-22']
2024-10-23 13:02:36,513 - aip.data.access - DEBUG - Making  dataset from raw data for dates ['2024-10-22']
2024-10-23 13:02:37,197 - aip.data.access - DEBUG - Writting file: /home/aip/AIP/data/interim/daily.conn.2024-10-22.csv.gz
2024-10-23 13:02:37,539 - aip.data.access - DEBUG - Writting file: /home/aip/AIP/data/processed/attacks.2024-10-22.csv.gz
2024-10-23 13:02:37,648 - aip.data.access - DEBUG - Creating attacks for dates ['2024-10-20', '2024-10-21']
...
```