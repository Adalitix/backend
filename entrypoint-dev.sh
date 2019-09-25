#!/bin/bash

# wait until a connection to postgres (db container) can be established
sh /home/devel/adalitix/backend/wait-for-db.sh

# Execute command provided as CMD (e.g.: runserver)
exec $@