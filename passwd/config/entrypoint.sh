#!/usr/bin/env bash

set -e

args=("$@")

case $1 in
    start-dev)
        exec ./config/start/start_dev_webserver.sh
        ;;
    *)
        exec "$@"
        ;;
esac
