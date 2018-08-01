#!/bin/bash

# apt-get install -y --force-yes netcat

set -e

host=$(env | grep _TCP_ADDR | cut -d = -f 2)
port=$(env | grep _TCP_PORT | cut -d = -f 2)

echo -n "waiting for TCP connection to $host:$port..."

while ! nc -w 1 $host $port 2>/dev/null
do
  echo -n .
  sleep 1
done

echo 'ok'
