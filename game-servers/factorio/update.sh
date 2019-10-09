#!/bin/bash
VERSION=$1

url=https://www.factorio.com/get-download/$VERSION/headless/linux64

if curl --output /dev/null --silent --head --fail "$url"; then
  docker build -t registry.npf.dk/gaas-factorio .
  docker tag registry.npf.dk/gaas-factorio registry.npf.dk/gaas-factorio:$VERSION
  docker push registry.npf.dk/gaas-factorio
  docker push registry.npf.dk/gaas-factorio:$VERSION
  echo $VERSION
else
  echo "URL does not exist: $url"
fi
