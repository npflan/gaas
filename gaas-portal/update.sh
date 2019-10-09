#!/bin/bash
VERSION=$(date +%s)
docker build -t registry.npf.dk/gaas-portal --no-cache .
docker tag registry.npf.dk/gaas-portal registry.npf.dk/gaas-portal:$VERSION
docker push registry.npf.dk/gaas-portal:$VERSION
docker push registry.npf.dk/gaas-portal
kubectl set image deployment/gaas-portal gaas-portal=registry.npf.dk/gaas-portal:$VERSION -n gaas
