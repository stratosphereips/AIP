import os
import csv
import datetime

print("Hello World")

data_directory = os.environ['output_data_folder']

files = os.listdir(str(data_directory))

dataset = dict()
for file in files:
    with open(data_directory + file, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        rows = list(reader)
        for row in rows:
            if row['SrcAddr'] not in dataset:
                total_events = 1
                total_duration = row['Dur']
                average_duration = row['Dur']
                total_bytes = row['TotBytes']
                average_bytes = row['TotBytes']
                total_packets = row['TotPkts']
                average_packets = row['TotPkts']
                last_event_time = float(datetime.datetime.strptime(row['StartTime'], '%Y/%m/%d %H:%M:%S.%f').strftime("%s"))
                dataset[row['SrcAddr']] = [total_events, total_duration, average_duration, total_bytes, average_bytes, total_packets, average_packets, last_event_time]
            else:
                past_data = row['SrcAddr']

                total_events = 1 + past_data[0]
                total_duration = row['Dur'] + past_data[1]
                average_duration = (row['Dur'] + (past_data[0]*past_data[2]))/total_events
                total_bytes = row['TotBytes'] + past_data[3]
                average_bytes = (row['TotBytes'] + (past_data[0]*past_data[4]))/total_events
                total_packets = row['TotPkts'] + past_data[5]
                average_packets = (row['TotPkts'] + (past_data[0]*past_data[6]))/total_events
                last_event_time = float(max([past_data]))
                datetime.datetime.strptime(row['StartTime'], '%Y/%m/%d %H:%M:%S.%f').strftime("%s"))

