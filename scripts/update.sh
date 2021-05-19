#!/usr/bin/bash

filename=$(date +%Y-%m-%d).csv
base_dir="/home/ground/projects/tickets-search-system"
db_url="jdbc:postgresql://localhost:5432/ground"
db_username="ground"
db_password="ground"

echo "======== 机票数据更新 ========"

if [[ -f "$base_dir"/data/flights.csv ]]; then
  hadoop fs -put "$base_dir"/data/flights.csv /warehouse/dws-flight/"$filename"
  mv "$base_dir"/data/flights.csv "$base_dir"/data/flights/"$filename"
  echo "文件上传成功：flights.csv >> $filename"

  hadoop fs -rm /warehouse/ads-ticket/'*'
  hive -e \
    "insert overwrite table flight.ads_ticket
      select flight_num,
      dcity_code,
      dairport_code,
      to_date(dtime),
      substr(dtime, 12, 8),
      acity_code,
      aairport_code,
      to_date(atime),
      substr(atime, 12, 8),
      airline_code,
      concat(plane, plane_code),
      plane_kind,
      price,
      discount,
      class,
      cdate
    from flight.dws_flight
    where cdate = current_date();"

  /home/ground/bigdata/sqoop/bin/sqoop export \
    --connect $db_url \
    --username $db_username \
    --password $db_password \
    --table ticket \
    --columns \
      "flight_num,
      dcity_code,
      dairport_code,
      ddate,
      dtime,
      acity_code,
      aairport_code,
      adate,
      atime,
      airline_code,
      aircraft,
      aircraft_type,
      price,
      discount,
      class,
      cdate" \
    --export-dir "hdfs://localhost:9000/warehouse/ads-ticket" \
    --input-fields-terminated-by ','

  source "$base_dir"/.pyenv/bin/activate
  python "$base_dir"/ml/predict.py

else
  echo "文件 flights.csv 不存在"
fi

printf "\n====== 最低价格数据更新 ======\n"

if [[ -f "$base_dir"/data/prices.csv ]]; then
  hadoop fs -put "$base_dir"/data/prices.csv /warehouse/dws-price/"$filename"
  mv "$base_dir"/data/prices.csv "$base_dir"/data/prices/"$filename"
  echo "文件上传成功：prices.csv >> $filename"

  hadoop fs -rm /warehouse/ads-price/'*'
  hive -e \
    "insert overwrite table flight.ads_price
    select dcity_code,
      acity_code,
      ddate,
      day,
      price,
      substr(flight_num, 0, 6),
      airline_code,
      airline,
      cdate
    from flight.dws_price
    where cdate = current_date();"

  /home/ground/bigdata/sqoop/bin/sqoop export \
    --connect $db_url \
    --username $db_username \
    --password $db_password \
    --table low_price \
    --columns \
      "dcity_code,
      acity_code,
      ddate,
      day,
      price,
      flight_num,
      airline_code,
      airline,
      cdate" \
    --export-dir "hdfs://localhost:9000/warehouse/ads-price" \
    --input-fields-terminated-by ','

else
  echo "文件 prices.csv 不存在"
fi
