#!/usr/bin/bash

hive -e "insert overwrite table flight.ads_airline
select distinct airline_code,
       airline
from flight.dws_flight;"

/home/ground/bigdata/sqoop/bin/sqoop export \
  --connect jdbc:postgresql://localhost:5432/ground \
  --username ground \
  --password ground \
  --table airline \
  --columns "code,name" \
  --export-dir "/warehouse/ads-airline" \
  --input-fields-terminated-by ','
