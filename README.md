# The Attacker IP Prioritizer V2.0.1


## The Idea

The Attacker IP Prioritizer (AIP) algorithm aims to generate a IoT friendly blacklist. With the advent of 5G, many IoT devices are going to be directly connected to the internet instead of being protected by a routers firewall. Therefore we need blacklists that are small and portable, and designed to blacklist IPs that are targeting IoT. The IPs of interest, from a statistics point of view, should have a couple of recognizable features:

First, they should be attacking more often than other IPs. In terms of our collected training data, we increase the priority of the IPs that attack more.

Second, IPs should attack consistently. Namely, IPs should have a higher daily average of attacks and its standard deviation should be lower.

Third, the average duration of the attacks should be longer. This is simply because larger and more advanced botnets are more organized and thorough, thus meaning they need to try more things once they get into our honeypots, thus increasing the length of their events.

Fourth, IPs should be currently active. An IP that was last seen a few months ago would have its priority decreased in our list.

Fifth, the number of bytes transferred and the number of packets sent and received will be greater.

All five of these traits need to be included in the sorting process of AIP and each of them needs to be weighted since they are not of equal importance. Therefore, there is a need to build a prioritization algorithm that receives data flows and outputs information built on top of these six characteristics.

## Data Source

What to program accepts is a directory that contains data files from each day. You assign a directory for the program to look in every time it runs, and it checks if there are any new files to process. If there are, it processes the new files and remembers the names of the new files so that it does not process it the next time it runs.

In terms of file format, it accepts a .csv file that has one IP per line, with each of the following data inputs for each IP on that line, separated by commas:

    Amount of events - Meaning the total connections to our honeypots originating from the given IP

    Total Duration - How long did this IP connect for the total of its events

    Average duration - The average length in seconds of all the connections per IP

    Amount of Bytes - Total bytes sent and received

    Average number of bytes - For bytes transferred in each connection per IP

    Total packets - Of all the connections per IP

    Average packets - Average packets sent per connection

    Last event time - UNIX time of the last time the IP tried to connect to something  in the last 24 hours

    First event time - UNIX time of the first time the IP tried to connect in the last 24 hours

For example, a single line in the file could look like this:

"IPv4 Addrss",26049,"7415310","284.6","41808957","1605.0",284577,"10.92","157899154","1578968762.519"

## The AIP Algorithm

The AIP algorithm takes each of the flows from the input and uses its data to calculate eight values for each IP. The first seven values from the input data remain unchanged, number of events, total duration, average duration, number of bytes, the average number of bytes, total packets and average packets. However, the first event time and the number of events are used to calculate the average number of events per day the IP has had since it was first seen by the program, giving us a total of eight features as input for our algorithm.

For each IP, each of the eight values is updated using the data from the current day and then saved to a file, called the absolute file.  The absolute data file contains the values for all the IPs seen since the program was started.

The next step is to feed the absolute data file, which has been updated with the last 24 hours of events, into the rating program. The rating program assigns each of the eight values a specific weight. These weights control the effect each value will have on the final score. The sum of all weights is one.

Each feature is multiplied by its weight and then summed with the rest, as in a basic linear combination. Then the sum is multiplied by a time modifier. The program currently has three different modules each with its own time modifier, one prioritizing historically aggressive IPs, one prioritizing newer aggressive IPs and one only dealing with IPs seen in the last 24 hours.
