#!/bin/bash
VERSION=$(date +%s)
docker build -t registry.npf.dk/gaas-api --no-cache .
docker tag registry.npf.dk/gaas-api registry.npf.dk/gaas-api:$VERSION
docker push registry.npf.dk/gaas-api:$VERSION
docker push registry.npf.dk/gaas-api
kubectl set image deployment/gaas-api gaas-api=registry.npf.dk/gaas-api:$VERSION -n gaas
