#!/bin/sh

tr -d \' \
    | sed -E 's/.*, ([a-z]+),.*chosen=\[([a-z+, ]*)\].*/\1,\2/' \
    | tr -d " "