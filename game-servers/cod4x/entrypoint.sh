#!/bin/sh
printf " =========================================\n"
printf " =========================================\n"
printf " ======== COD4X Dedicated Server =========\n"
printf " =========================================\n"
printf " =========================================\n"
printf " ============== by NPFLAN ================\n\n"

exitOnError(){
  status=$1
  message=$2
  [ "$message" != "" ] || message="Error!"
  if [ $status != 0 ]; then
    printf "$message (status $status)\n"
    exit $status
  fi
}

if [ ! -f main/xbase_00.iwd ]; then
  cp xbase_00.iwd main/xbase_00.iwd
fi
exitOnError $?
if [ ! -f main/server.cfg ]; then
  cp server.cfg main/server.cfg
fi
exitOnError $?
printf "COD4X arguments are: $@\n\n"
./cod4x18_dedrun +set fs_homepath /home/user/cod4"$@"
status=$?
printf "\n =========================================\n"
printf " Exit with status $status\n"
printf " =========================================\n"
