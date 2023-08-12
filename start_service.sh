#!/bin/bash
cd /home/elk_web/
source elk_web.sh
flask migrate db init
flaks migrate db migrate
systemctl start elk_web.service
systemctl start nginx.service
tail -f /dev/null
