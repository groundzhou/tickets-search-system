#!/usr/bin/bash

filename=$(date +%Y-%m-%d).csv
base_dir="/home/ground/projects/tickets-search-system"

if [[ -f "$base_dir"/data/flights.csv ]]; then
  hadoop fs -put "$base_dir"/data/flights.csv /warehouse/dws-flight/"$filename"
  mv "$base_dir"/data/flights.csv "$base_dir"/data/flights/"$filename"
  echo "文件上传成功：flights.csv >> $filename"
else
  echo "文件 flights.csv 不存在"
fi

if [[ -f "$base_dir"/data/prices.csv ]]; then
  hadoop fs -put "$base_dir"/data/prices.csv /warehouse/dws-price/"$filename"
  mv "$base_dir"/data/prices.csv  "$base_dir"/data/prices/"$filename"
  echo "文件上传成功：prices.csv >> $filename"
else
  echo "文件 prices.csv 不存在"
fi
