#!/usr/bin/env bash
T0=$(cat "$(dirname "$0")/run/T0"); NOW=$(date -u +%s); E=$((NOW-T0))
printf "elapsed %02d:%02d | to 12h %+d min | to freeze(15h) %+d min | to stop(16h) %+d min\n" \
  $((E/3600)) $((E%3600/60)) $(( (43200-E)/60 )) $(( (54000-E)/60 )) $(( (57600-E)/60 ))
