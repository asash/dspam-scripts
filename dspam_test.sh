#! /bin/sh
IN_DIR=$1
DEBUG="on"

DEBUG_KEY=""

if [ "$DEBUG" = "on" ]; then
    DEBUG_KEY="--debug"
fi

for EMAIL in `ls -1 $IN_DIR`; do
    RESULT=`dspam --user firexel --mode=notrain $DEBUGKEY --deliver=summary --stdout < $IN_DIR/$EMAIL\
        | grep -oP 'result=".*?"' | grep -oP 'Spam|Innocent'`
    echo $RESULT
done

