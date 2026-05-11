#!/bin/bash
set -eo pipefail

user="${POSTGRES_USER:-postgres}"
db="${POSTGRES_DB:-$user}"
export PGPASSWORD="${POSTGRES_PASSWORD:-}"

if pg_isready -U "$user" -d "$db"; then
  exit 0
fi

exit 1
