#!/bin/bash
size=$[$#/3]
arr=("$@")
for((i=0;i<$size;i++))
     do
       k1=$[$i*3]
       k2=$[$i*3+1]
       k3=$[$i*3+2]
   echo $((${arr[k1]}${arr[k2]}${arr[k3]}))
     done




