#!/bin/bash
clear

echo " "
echo "GOES16 GLM descarga"

USER='arturo66cta@gmail.com'
PASS='Mazamorra2328'

n=1
for x in $(cat /mnt/Data/Data/IMERG/download/IMERG_2021_03_2021_08.txt);do

	NAME1=$(echo $x | cut -d"/" -f9)
	NAME2=$(echo $NAME1 | cut -d"?" -f1)
	NAME3="/mnt/Data/Data/IMERG/download/$NAME2"

	if [ \( $n -eq 0 \) -o \( $n -eq 1 \) ]
	then
		echo "Cabezales"
	else
		echo $n,$NAME2
		if [ -f $NAME3 ]
		then
			echo "Archivo existe"
		else
			echo "Descargando"
			wget --user $USER --password $PASS $x -O $NAME3
		fi
	fi
	echo ""
	n=$((n+1))

done
