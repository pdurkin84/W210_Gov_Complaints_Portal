#!/bin/bash
# Set up iptables
logger "W210: Installing and configuring iptables to allow only ssh on the public address"
mkdir /etc/iptables
curl http://10.187.254.196/Files/rules.v4 > /etc/iptables/rules.v4
chmod go-rwx /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4
DEBIAN_FRONTEND=noninteractive apt-get -y -q install iptables-persistent
logger "W210: Completed iptables"
