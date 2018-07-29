#!/bin/bash
array=( "0" "107" "348" "414" "686" "698" "1684" "1912" "3437" "3980" )
for i in "${array[@]}"
do
   echo "$i"
   python code.py $i
   # or do whatever with individual element of the array
done