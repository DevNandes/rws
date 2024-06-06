#!/bin/csh -f

# ABSTRACT: Script de inicializacao do rws
#
# "Mas ele foi traspassado pelas nossas transgressoes e moido pelas nossas
# iniquidades; o castigo que nos traz a paz estava sobre ele, e pelas
# suas pisaduras fomos sarados." Isaias 53.5

# Fine tuning >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7
#
# The suggested number of workers is (2*CPU)+1
# The maximum concurrent requests are workers * threads
# 3 CPUs:
#   number of workers = (2 * 3) + 1 = 7
#   workers = 3
#   threads = 2
#   max concurrent requets = (3 * 2) = 6
#
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


source /etc/csh.cshrc

exec gunicorn wsgi:application \
    --name=rws \
    --bind=${RUN_HOST}:${RUN_PORT} \
    --workers=3 \
    --threads=2 \
    --log-level=info \
    --log-file=${LOGS_DIR}/gunicorn.log \
    --access-logfile=${LOGS_DIR}/gunicorn-access.log \
    --timeout=600


# exec sh -c "while true; do sleep 1; done"


# EOF
