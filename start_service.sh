#!/bin/bash
cd /home/elk_web/
source elk_web.sh
flask db init
flask db migrate
flask db upgrade
systemctl start elk_web.service
systemctl start nginx.service
tail -f /dev/null
