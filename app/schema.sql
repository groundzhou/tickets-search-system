DROP TABLE IF EXISTS ground.ticket;
DROP TABLE IF EXISTS ground.provider;
DROP TABLE IF EXISTS ground.airline;
DROP TABLE IF EXISTS ground.airport;
DROP TABLE IF EXISTS ground.city;
DROP TABLE IF EXISTS ground.bjs_kmg_price;
DROP TABLE IF EXISTS ground.low_price;

-- 城市列表
CREATE TABLE ground.city
(
    id   serial PRIMARY KEY NOT NULL,
    name varchar(80)        NOT NULL,
    code char(3)            NOT NULL UNIQUE
);

-- 机场列表
CREATE TABLE ground.airport
(
    id        serial PRIMARY KEY,
    name      varchar(120) NOT NULL,
    code      char(3)      NOT NULL UNIQUE,
    city_code char(3) REFERENCES ground.city (code)
);

-- 航空公司
CREATE TABLE ground.airline
(
    id   serial PRIMARY KEY,
    code char(2) NOT NULL UNIQUE,
    name varchar(120) NOT NULL
);

-- 机票信息
CREATE TABLE ground.ticket
(
    id            serial PRIMARY KEY,
    flight_num    char(6),
    dcity_code    char(3),
    dairport_code char(3),
    ddate         date,
    dtime         time,
    acity_code    char(3),
    aairport_code char(3),
    adate         date,
    atime         time,
    airline_code  char(2),
    aircraft      varchar(20),
    aircraft_type varchar(20),
    price         int4,
    discount      float4,
    class         varchar(20),
    cdate         date
);

-- 供应商
CREATE TABLE ground.provider
(
    id        serial PRIMARY KEY NOT NULL,
    name      varchar(80)        NOT NULL,
    site      varchar(240),
    icon_path varchar(240)
);

-- 北京至昆明价格预测
CREATE TABLE ground.bjs_kmg_price
(
    id         serial PRIMARY KEY NOT NULL,
    ticket_id  int4,
    price      float4,
    cdate      date
);

-- 每日最低票价
CREATE TABLE ground.low_price
(
    id           serial PRIMARY KEY,
    dcity_code   char(3),
    acity_code   char(3),
    ddate        date,
    day          int4,
    price        int4,
    flight_num   char(6),
    airline_code char(2),
    airline      varchar(80),
    cdate        date
);