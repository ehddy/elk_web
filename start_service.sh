#!/bin/bash
cd /home/elk_web/
source elk_web.sh
flask migrate db init
flask migrate db migrate
tail -f /dev/null
