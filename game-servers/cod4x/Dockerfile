FROM qmcgaw/cod4

COPY --chown=1000 libs/main/ main/
COPY --chown=1000 libs/zone/ zone/

COPY --chown=1000 entrypoint.sh ./
COPY --chown=1000 server.cfg ./
RUN chmod +x entrypoint.sh
RUN rm -f main/q3config_server.cfg
EXPOSE 28960/tcp
ENTRYPOINT [ "/home/user/cod4/entrypoint.sh" ]
CMD +set dedicated 2 +set sv_cheats "0" +set sv_maxclients "32" +exec server.cfg +gametype ffa +map mp_killhouse 
USER root
