#!/bin/bash
docker run --rm --name gaas-portal -p 8080:80 -v nginx:/etc/nginx/conf.d/ -v /Users/jesperpetersen/Dropbox/gaas/gaas-portal/static:/usr/share/nginx/html/ nginx:alpine
