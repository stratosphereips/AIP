import os
import csv
import datetime

print("Hello World")

data_directory = os.environ['output_data_folder']

output = os.environ['results_file']

files = os.listdir(str(data_directory))

dataset = dict()
for file in files:
    print(file)
    with open(data_directory + file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        rows = list(reader)
        for row in rows:
            # System Ports (0-1023), User Ports (1024-49151), and the Dynamic and/or Private Ports (49152-65535);
            try:
                if int(row['Sport']) >= 10000:
                    if row['SrcAddr'] not in dataset.keys():
                        total_events = 1
                        total_duration = float(row['Dur'])
                        average_duration = float(row['Dur'])
                        total_bytes = float(row['TotBytes'])
                        average_bytes = float(row['TotBytes'])
                        total_packets = float(row['TotPkts'])
                        average_packets = float(row['TotPkts'])
                        last_event_time = float(datetime.datetime.strptime(row['StartTime'], '%Y/%m/%d %H:%M:%S.%f').strftime("%s"))
                        first_event_time = float(datetime.datetime.strptime(row['StartTime'], '%Y/%m/%d %H:%M:%S.%f').strftime("%s"))
                        dataset[row['SrcAddr']] = {"SrcAddr": row['SrcAddr'], "total_events": total_events,
                                                   "total_duration": total_duration,
                                                   "average_duration": average_duration, "total_bytes": total_bytes,
                                                   "average_bytes": average_bytes,
                                                   "total_packets": total_packets, "average_packets": average_packets,
                                                   "last_event_time": last_event_time,
                                                   "first_event_time": first_event_time}
                    else:
                        past_data = dataset[row['SrcAddr']]
                        total_events = 1 + past_data["total_events"]
                        total_duration = float(row['Dur']) + past_data["total_duration"]
                        average_duration = (float(row['Dur']) + (past_data["total_events"]*past_data["average_duration"]))/total_events
                        total_bytes = float(row['TotBytes']) + past_data["total_bytes"]
                        average_bytes = (float(row['TotBytes']) + (past_data["total_events"]*past_data["average_bytes"]))/total_events
                        total_packets = float(row['TotPkts']) + past_data["total_packets"]
                        average_packets = (float(row['TotPkts']) + (past_data["total_events"]*past_data["average_packets"]))/total_events
                        last_event_time = float(max([past_data["last_event_time"], float(datetime.datetime.strptime(row['StartTime'], '%Y/%m/%d %H:%M:%S.%f').strftime("%s"))]))
                        first_event_time_event_time = float(min([past_data["first_event_time"], float(
                            datetime.datetime.strptime(row['StartTime'], '%Y/%m/%d %H:%M:%S.%f').strftime("%s"))]))
                        dataset[row['SrcAddr']] = {"SrcAddr": row['SrcAddr'], "total_events": total_events,
                                                   "total_duration": total_duration,
                                                   "average_duration": average_duration, "total_bytes": total_bytes,
                                                   "average_bytes": average_bytes,
                                                   "total_packets": total_packets, "average_packets": average_packets,
                                                   "last_event_time": last_event_time,
                                                   "first_event_time": first_event_time}
                else:
                    continue
            except ValueError as x:
                continue

list_of_dictionaries = []
print(len(list_of_dictionaries))
for key in dataset.keys():
    list_of_dictionaries.append(dataset[key])

labels = ["SrcAddr", "total_events", "total_duration", "average_duration", "total_bytes", "average_bytes", "total_packets",
          "average_packets", "last_event_time", "first_event_time"]

try:
    with open(output, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
        for elem in list_of_dictionaries:
            writer.writerow(elem)
except IOError:
    print("I/O error")
