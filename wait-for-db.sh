#!/usr/bin/env bash

cmd="$@"

# wait until a connection to postgres can be established
until PGPASSWORD=adalitix psql -h "db" -U "adalitix" -c '\q' > /dev/null 2>&1; do
  >&2 echo "Waiting for Postgres container..."
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Execute provided command
exec ${cmd}