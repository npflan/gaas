#!/bin/bash
BIN=./bin/x64/factorio
SAVES_DIR=/factorio/saves
SAVE=$SAVES_DIR/save.zip

[[ -f $SAVE ]] && EXISTING_SAVE="yes"
[[ -f $SAVE ]] || $BIN --create $SAVE

JQ_FILTER=""

[[ -n $SERVER_NAME ]] && JQ_FILTER="$JQ_FILTER .name = \"$SERVER_NAME\" |"
[[ -n $SERVER_DESCRIPTION ]] && JQ_FILTER="$JQ_FILTER .description = \"$SERVER_DESCRIPTION\" |"
[[ -n $PUBLIC ]] && JQ_FILTER="$JQ_FILTER .visibility.public = \"$PUBLIC\" |"

JQ_FILTER="$JQ_FILTER ."

jq "$JQ_FILTER" data/server-settings.example.json > data/server-settings.json

exec $BIN \
  --start-server-load-latest \
  --server-settings /factorio/data/server-settings.json \
  --bind 0.0.0.0 \
  --no-log-rotation
