#!/bin/bash
cd /home/elk_web/
source elk_web.sh
ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
flask db init
flask db migrate
flask db upgrade
python create_superuser.py
systemctl start elk_web.service
systemctl restart nginx
tail -f /dev/null
