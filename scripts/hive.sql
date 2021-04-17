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