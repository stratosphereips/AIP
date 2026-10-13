# Docker image for AIP

The Docker image includes AIP and everything it needs to run. Your Zeek logs and the AIP `data/` folder stay on your machine and are shared with the container when you run it.

## Build the image

```bash
git clone https://github.com/stratosphereips/AIP.git
cd AIP/
docker build --build-arg uid=1000 --file etc/docker/Dockerfile --tag aip:latest .
```

## Prepare the data

AIP reads Zeek logs. These steps assume your Zeek logs are in `/opt/zeek/logs/`.

Copy the two example files and edit the copies:

```bash
cp data/external/honeypots_public_ips_example.csv data/external/honeypots_public_ips.csv
cp data/external/do_not_block_these_ips_example.csv data/external/do_not_block_these_ips.csv
```

- `honeypots_public_ips.csv` (required): the public IPs of your honeypots. AIP only looks at traffic sent to these IPs.
- `do_not_block_these_ips.csv` (optional): IPs that must never appear in a blocklist.

## Run the container

Run all models for today:

```bash
docker run --rm \
  -v /opt/zeek/logs/:/home/aip/AIP/data/raw:ro \
  -v ${PWD}/data/:/home/aip/AIP/data/:rw \
  --name aip aip:latest bin/aip
```

Run all models for one day, showing full detail with `-d`:

```bash
docker run --rm \
  -v /opt/zeek/logs/:/home/aip/AIP/data/raw:ro \
  -v ${PWD}/data/:/home/aip/AIP/data/:rw \
  --name aip aip:latest bin/aip -d run-models --start-date 2024-10-22 --end-date 2024-10-22
```

The output starts like this:

```
2024-10-23 13:02:36,513 - aip.data.access - DEBUG - Creating attacks for dates ['2024-10-22']
2024-10-23 13:02:36,513 - aip.data.access - DEBUG - Making  dataset from raw data for dates ['2024-10-22']
2024-10-23 13:02:37,197 - aip.data.access - DEBUG - Writting file: /home/aip/AIP/data/interim/daily.conn.2024-10-22.csv.gz
2024-10-23 13:02:37,539 - aip.data.access - DEBUG - Writting file: /home/aip/AIP/data/processed/attacks.2024-10-22.csv.gz
2024-10-23 13:02:37,648 - aip.data.access - DEBUG - Creating attacks for dates ['2024-10-20', '2024-10-21']
...
```

Without `-v` or `-d`, AIP only prints errors. Blocklists are saved in `data/output/`. See the [main README](../../README.md#commands) for all commands.
