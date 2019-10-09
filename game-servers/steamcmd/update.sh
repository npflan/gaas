#!/bin/bash
VERSION=$(date +%s)
docker build -t cytram/gaas-steamcmd .
docker tag cytram/gaas-steamcmd cytram/gaas-steamcmd:$VERSION
docker push cytram/gaas-steamcmd
docker push cytram/gaas-steamcmd:$VERSION
echo $VERSION#!/bin/bash
