# Attacker IP Prioritization (AIP) Tool
The Attacker IP Prioritization (AIP) is a tool to generate IP blocklists based on network traffic captured from honeypot networks. Originally designed to create the blocklists for the [Stratosphere Blocklist Generation project](https://mcfp.felk.cvut.cz/publicDatasets/CTU-AIPP-BlackList/), it aims to generate an IoT-friendly blocklist. With the advent of 5G, IoT devices will be directly connected to the Internet instead of being protected by a router's firewall. Therefore we need blocklists that are small and portable and designed to block those IPs that are targeting IoT devices. The main models used to this end are the Prioritize Consistent and the Prioritize New.


Eventually, the project evolved, aiming to test new blocklists generation models beyond the PN and PC. The actual codebase allows a fast developing and testing of those new models, providing a common interface to access the attacks from several sensors deployed on the Public Internet, and a common set of metrics to compare the output of the models.


Given a honeypot network in your organization, it should be easy to use AIP to generate your own local blocklists based on the traffic reaching the honeypots.

![Description of the AIP pipeline](images/AIP_Diagram.png "AIP Tool pipeline")

## Installing the development environment

### What will you need
* Docker - We will clone a repo and build a docker image locally. You should be fine if "docker run hello-world" works on your machine.
* Disk space. The base dataset to generate blocklists is 39 MB. However, some models like Prioritize New, Prioritize Consistent, or Random Forest generates a massive amount of intermediate data.
* Ipython or Jupyter to load and plot Pandas DataFrames (optional).
* Python coding skills (highly recommended).
The steps of this tutorial were tested on a Linux machine. Some Docker magic may only work on some platforms. Please report successful and unsuccessful attempts using other platforms.

