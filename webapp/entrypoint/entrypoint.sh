#!/usr/bin/env bash

set -e

args=("$@")

case $1 in
    start-webserver-dev)
        exec ./entrypoint/webserver/start_dev.sh
        ;;
    start-webserver-prod)
        exec ./entrypoint/webserver/start_prod.sh
        ;;
    *)
        exec "$@"
        ;;
esac
