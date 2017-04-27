#!/bin/bash

echo "Purge unnecessary packages"
# apt purge sonic-pi minecraft-pi wolfram-engine -y && apt-get autoremove -y

echo "Upgrading system..."
# apt update
# apt upgrade -y

echo "Installing packages..."
# apt install qupzilla
# pip install -U evdev netifaces

echo "Installing configs..."
cp logrotate/barcodescanner-pi /etc/logrotate.d/
cp systemd/barcodescanner-pi.service /lib/systemd/system/barcodescanner-pi.service
cp udev/90-barcode.rules /etc/udev/rules.d/90-barcode.rules
chown root:root /lib/systemd/system/barcodescanner-pi.service; chmod 644 /lib/systemd/system/barcodescanner-pi.service
chown root:root /etc/logrotate.d/barcodescanner-pi; chmod 644 /etc/logrotate.d/barcodescanner-pi
chown root:root /etc/udev/rules.d/90-barcode.rules; chmod 644 /etc/udev/rules.d/90-barcode.rules
systemctl daemon-reload
systemctl enable barcodescanner-pi.service
reboot
