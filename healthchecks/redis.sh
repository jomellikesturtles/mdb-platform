#!/bin/sh
set -eo pipefail

if [ "$(redis-cli ping)" = "PONG" ]; then
  exit 0
fi

exit 1
