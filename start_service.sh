#!/bin/bash
cd /home/elk_web/
source elk_web.sh
flask db init
flask db migrate
tail -f /dev/null
