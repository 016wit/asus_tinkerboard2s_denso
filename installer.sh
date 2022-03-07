#!/bin/bash
pip3 install virtualenv
echo "Install gpio service"
tar xf pi-io.tar.gz
cd pi-io \
  && virtualenv venv \
  && source venv/bin/activate \
  && pip3 install -r requirements.txt \
  && deactivate \
  && cd /home/linaro

echo "Disable black screen and screen saver"
sed -i "s/\#xserver-command=X/xserver-command=X -s 0 dpms/g" /etc/lightdm/lightdm.conf \
  && sh -c  'echo "/usr/bin/chromium-browser --start-fullscreen --disable-restore-session-state --incognito http://localhost" >> /etc/xdg/lxsession/LXDE-pi/autostart'

echo "Setting up service"
ln -s /home/linaro/pi-io/gpio.service /etc/systemd/system/gpio.service

systemctl enable gpio.service

systemctl daemon-reload
systemctl start gpio.service
echo "Install complete"
echo "Setup RTC"
./rtc_setup.sh -u rtc_ds3231
systemctl disable systemd-timesyncd.service
./ins_script.sh
rm pi-io.tar.gz installer.tar.gz
echo "Reboot system"
reboot
