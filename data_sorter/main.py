"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
"""
#! /usr/local/bin/python3

import csv
import os
from datetime import datetime
from logging import getLogger

from slips_aip_constants.defaults import Defaults, EnvVars


logger = getLogger(__name__)


logger.info("AIP: Hello world")

data_directory = os.environ[EnvVars.OUTPUT_DATA_FOLDER.value]
output = os.environ[EnvVars.RESULTS_FILE.value]
files = os.listdir(data_directory)

dataset = {}
for file in files:
    logger.debug(f"Filename: {file}")
    with open(f"{data_directory}{file}", "r", encoding=Defaults.UTF_8.value) as f:
        reader = csv.DictReader(f, delimiter=',')
        rows = list(reader)
        for row in rows:
            # System Ports (0-1023), User Ports (1024-49151), and the Dynamic and/or Private Ports (49152-65535);
            try:
                if int(row['Sport']) >= 32000:
                    if row['SrcAddr'] not in dataset.keys():
                        total_events = 1
                        total_duration = float(row['Dur'])
                        average_duration = float(row['Dur'])
                        total_bytes = float(row['TotBytes'])
                        average_bytes = float(row['TotBytes'])
                        total_packets = float(row['TotPkts'])
                        average_packets = float(row['TotPkts'])
                        last_event_time = float(datetime.strptime(row['StartTime'], Defaults.SPLUNK_DATE_FORMAT.value).strftime("%s"))
                        first_event_time = float(datetime.strptime(row['StartTime'], Defaults.SPLUNK_DATE_FORMAT.value).strftime("%s"))
                        dataset[row['SrcAddr']] = {"SrcAddr": row['SrcAddr'],
                                                   "total_events": total_events,
                                                   "total_duration": total_duration,
                                                   "average_duration": average_duration,
                                                   "total_bytes": total_bytes,
                                                   "average_bytes": average_bytes,
                                                   "total_packets": total_packets,
                                                   "average_packets": average_packets,
                                                   "first_event_time": first_event_time,
                                                   "last_event_time": last_event_time}
                    else:
                        past_data = dataset[row['SrcAddr']]
                        total_events = 1 + past_data["total_events"]
                        total_duration = float(row['Dur']) + past_data["total_duration"]
                        average_duration = (float(row['Dur']) + (past_data["total_events"]*past_data["average_duration"]))/total_events
                        total_bytes = float(row['TotBytes']) + past_data["total_bytes"]
                        average_bytes = (float(row['TotBytes']) + (past_data["total_events"]*past_data["average_bytes"]))/total_events
                        total_packets = float(row['TotPkts']) + past_data["total_packets"]
                        average_packets = (float(row['TotPkts']) + (past_data["total_events"]*past_data["average_packets"]))/total_events
                        last_event_time = float(max([past_data["last_event_time"], float(datetime.strptime(row['StartTime'], Defaults.SPLUNK_DATE_FORMAT.value).strftime("%s"))]))
                        first_event_time_event_time = float(min([past_data["first_event_time"], float(datetime.strptime(row['StartTime'], Defaults.SPLUNK_DATE_FORMAT.value).strftime("%s"))]))
                        dataset[row['SrcAddr']] = {"SrcAddr": row['SrcAddr'],
                                                   "total_events": total_events,
                                                   "total_duration": total_duration,
                                                   "average_duration": average_duration, 
                                                   "total_bytes": total_bytes,
                                                   "average_bytes": average_bytes,
                                                   "total_packets": total_packets,
                                                   "average_packets": average_packets,
                                                   "first_event_time": first_event_time,
                                                   "last_event_time": last_event_time}

            except ValueError as x:
                continue

list_of_dictionaries = [dataset.get(key) for key in dataset.keys()]

labels = {"SrcAddr", "total_events", "total_duration", "average_duration", "total_bytes", "average_bytes", "total_packets",
          "average_packets", "first_event_time", "last_event_time"}

try:
    with open(output, "w", encoding=Defaults.UTF_8.value) as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
        for elem in list_of_dictionaries:
            writer.writerow(elem)
except IOError as e:
    logger.error(f"{output} I/O error: {e}")
