#!/bin/bash
VERSION=$(date +%s)
docker build -t cytram/gaas-base .
docker tag cytram/gaas-base cytram/gaas-base:$VERSION
docker push cytram/gaas-base
docker push cytram/gaas-base:$VERSION
echo $VERSION
