USE flight;

-- 航班数据
DROP TABLE IF EXISTS dws_flight;
CREATE EXTERNAL TABLE dws_flight
(
    dairport_code STRING,
    dairport      STRING,
    dterminal     STRING,
    dcity_code    STRING,
    dcity         STRING,
    aairport_code STRING,
    aairport      STRING,
    aterminal     STRING,
    acity_code    STRING,
    acity         STRING,
    airline_code  STRING,
    airline       STRING,
    flight_num    STRING,
    plane_code    STRING,
    plane_kind    STRING,
    plane         STRING,
    dtime         STRING,
    atime         STRING,
    price         INT,
    discount      DOUBLE,
    class         STRING,
    punctuality   INT,
    stop          INT,
    cdate         STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE LOCATION '/warehouse/dws-flight/';


-- 最低票价
DROP TABLE IF EXISTS dws_price;
CREATE EXTERNAL TABLE dws_price
(
    dcity_code   STRING,
    acity_code   STRING,
    ddate        STRING,
    day          INT,
    price        INT,
    discount     DOUBLE,
    flight_num   STRING,
    airline_code STRING,
    airline      STRING,
    cdate        STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE LOCATION '/warehouse/dws-price/';


-- 2019年北京至昆明数据
DROP TABLE IF EXISTS bjs_kmg;
CREATE EXTERNAL TABLE bjs_kmg
(
    flight_num    STRING,
    share         STRING,
    dtime         STRING,
    atime         STRING,
    ctime         STRING,
    discount      DOUBLE,
    price         INT,
    ahead         INT,
    dairport_code STRING,
    dcity_code    STRING,
    aairport_code STRING,
    acity_code    STRING,
    ddate         STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE LOCATION '/warehouse/bjs_kmg/';

-- 2019年北京至昆明数据
DROP TABLE IF EXISTS flight.bjs_kmg_2;
CREATE EXTERNAL TABLE flight.bjs_kmg_2
(
    airline  STRING,
    ddate    STRING,
    ahead    INT,
    dtime    INT,
    atime    INT,
    discount DOUBLE,
    price    INT
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE LOCATION '/warehouse/bjs_kmg_2/';

insert overwrite table flight.bjs_kmg_2
select substr(flight_num, 0, 2), ddate, ahead, hour(dtime), hour(atime), discount, price
from flight.bjs_kmg;


CREATE EXTERNAL TABLE test
(
    airline  STRING,
    ddate    STRING,
    ahead    INT,
    dtime    INT,
    atime    INT,
    discount DOUBLE,
    price    INT
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    STORED AS TEXTFILE LOCATION '/warehouse/test/';