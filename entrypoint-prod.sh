#!/usr/bin/env bash

# wait until a connection to postgres (db container) can be established
sh /home/devel/adalitix/backend/wait-for-db.sh

echo "Collect static files"
sudo chown -R devel:devel /home/devel/adalitix/backend/backend/static
python /home/devel/adalitix/backend/manage.py collectstatic --noinput

# Execute command provided as CMD (e.g.: runserver)
exec $@
