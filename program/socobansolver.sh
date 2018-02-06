#!/bin/bash

echo "Enter the file name of file with map description:"


read filename

a=1
let t1=$(date +%s)
let t2=$(date +%s)
let COUNT=`expr $t2 - $t1`


while :
do
    python SokobanSolver.py $filename $a > /dev/null || exit
    
    if [ $COUNT -gt 60 ]
    then
        break
    fi
    let t2=$(date +%s)
    let COUNT=`expr $t2 - $t1`
    
    minisat "outsat" "result" > /dev/null
    
    name=""
    while read -r line
    do
        name="$line"
        if [ "$name" == "UNSAT" ]
        then
            echo "UNSATISFIABLE for $a states"
            break
        fi
        
        if [ "$name" != "UNSAT" ]
        then
            name="SATISFIABLE"
            break
        fi
    done < "result"
    
    if [ "$name" == "SATISFIABLE" ]
        then
            echo "SATISFIABLE for $a states"
            python trueConverter.py
            echo "TRUE LITERALS:"
            cat "finalresult"
	    echo "Would like to see vizualization of result?[y/n]:"
	    read answer
	    if [ "$answer" == "y" ]
            then
            	java -jar SokobanVisulaziation.jar $filename "finalresult"
            break
        fi

            break
        fi
    
    let a+=1
done
