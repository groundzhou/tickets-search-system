#!/usr/bin/bash

/home/ground/bigdata/sqoop/bin/sqoop export \
--connect jdbc:postgresql://hadoop-1:5432/ground \
--username ground \
--password ground \
--table test \
--export-dir /warehouse/ads-flight \
--input-fields-terminated-by ','
