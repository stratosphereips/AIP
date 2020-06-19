Here is a quick explaination of the differnces between the different historical data folders in this directory.

New-Each-Day: This folder contains the blacklists for IPs seen attacking our honeypots for the first time in the 
last 24 hours. There is one file for each day since the the program has been running. 

Prioritize-Consistent: This folder contains the blacklists for IPs that were rated by the function that prioritizes
consistent and aggressive IPs over time. The ratings for each day were from all the data gathered since AIP was started. 
There is one file for each day.

Prioritize-New: This folder contains the blacklists for IPs that were rated by the function that prioritizes new IPs over 
older ones. The ratings for each day were from all the data gathered since AIP was started. There is one file for each day. 
