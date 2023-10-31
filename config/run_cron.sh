#!/bin/bash
if [[ "$CRON_PROCS" == "0" ]];
then
    echo "cron_jobs is has not started."
    sleep infinity
else
    rq worker -c py_rq_settings
fi
