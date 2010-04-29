#!/bin/bash

# compilzorz

# -D useparam : will try to make the game harder with time
# -D testperf : for testing speed of code
# -D nobackground : disable moving background
# -D debug : debugging facilities (god mode, adding enemies, ...), some asserts
# -D release : no debugging facilities, no asserts
# -D fpscounter

if [ -z "$1" ]
then
    echo "arguments: NAME MAIN [WIDTH=500 HEIGHT=500 COLOR=ffffff FPS=40]"
    exit
else
    NAME=$1
fi
if [ -z "$2" ]
then
    MAIN=$NAME
else
    MAIN=$2
fi
if [ -z "$3" ]
then
    HEIGHT=500
else
    HEIGHT=$3
fi
if [ -z "$4" ]
then
    WIDTH=$HEIGHT
else
    WIDTH=$4
fi
if [ -z "$5" ]
then
    COLOR=ffffff
else
    COLOR=$5
fi
if [ -z "$6" ]
then
    FPS=40
else
    FPS=$6
fi



#NAME=$1
#MAIN=$2
#WIDTH=500
#HEIGHT=500
#COLOR=ffffff
#FPS=40

TITLE=$MAIN
SWF=$NAME.swf
HTML=$NAME.html

~/haxe -swf $SWF -main $MAIN -swf-version 9 -swf-header $WIDTH:$HEIGHT:$FPS:$COLOR

cat ../data/default.html | sed -e "s/<<NAME>>/$NAME/g" -e "s/<<TITLE>>/$TITLE/g" -e "s/<<WIDTH>>/$WIDTH/g" -e "s/<<HEIGHT>>/$HEIGHT/g" -e "s/<<COLOR>>/$COLOR/g" > $HTML
