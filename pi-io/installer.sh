#!/bin/bash
cp gpio.service /etc/systemd/system/gpio.service
systemctl enable gpio.service
systemctl daemon-reload
systemctl start gpio.service
