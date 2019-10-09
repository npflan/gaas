#!/bin/bash
VERSION=$(date +%s)
docker build --build-arg CACHE_DATE="$(date)" -t registry.npf.dk/gaas-csgo .
docker tag registry.npf.dk/gaas-csgo registry.npf.dk/gaas-csgo:$VERSION
docker push registry.npf.dk/gaas-csgo
docker push registry.npf.dk/gaas-csgo:$VERSION
echo $VERSION
