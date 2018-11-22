#!/bin/bash -e
echo "starting cron job"
python3.6 /W210_Gov_Complaints_Portal/Code/REST/classify-pending-cron.py
echo "cron job done"

exit 0
