#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

export PGPASSWORD="Alfapostgre2608"

echo "Checking Postgres at host: $host"
until psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd