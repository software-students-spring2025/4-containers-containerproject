#!/bin/bash

# Use the db dump jumping-jack-db to seed the db
if [ -f /data/restore/users.bson ]; then
  mongorestore --drop --db=jumping-jack-db --collection=users /data/restore/users.bson
fi