#!/bin/bash

systemctl start elk_web.service
systemctl start nginx.service
tail -f /dev/null
