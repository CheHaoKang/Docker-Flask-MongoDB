#!/usr/bin/env bash
echo "Creating mongo users..."
mongo --authenticationDatabase admin --host localhost -u myUserAdmin -p abc123 Pluvio --eval "db.createUser({user: 'deckenkang66', pwd: '97155434', roles: [{role: 'readWrite', db: 'Pluvio'}]});"
echo "Mongo users created."
