#!/usr/bin/env bash

systemctl stop unattended-upgrades.service
while(pgrep -a apt-get); do sleep 1; done
export DEBIAN_FRONTEND=noninteractive
apt-get -V -y install linux-generic
reboot
