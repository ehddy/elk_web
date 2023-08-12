#!/bin/bash
cd /home/elk_web
export FLASK_APP=monitoring
export FLASK_DEBUG=true
export APP_CONFIG_FILE=/home/elk_web/config/developement.py
flask db init
tail -f /dev/null

