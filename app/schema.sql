-- 城市列表
DROP TABLE IF EXISTS ground.city;
CREATE TABLE ground.city
(
    id   serial PRIMARY KEY NOT NULL,
    name varchar(80)        NOT NULL,
    code char(3)            NOT NULL UNIQUE
);

-- 机场列表
DROP TABLE IF EXISTS ground.airport;
CREATE TABLE ground.airport
(
    id        serial PRIMARY KEY,
    name      varchar(120) NOT NULL,
    code      char(3)      NOT NULL UNIQUE,
    city_code char(3) REFERENCES ground.city (code)
);

-- 航空公司
DROP TABLE IF EXISTS ground.airline;
CREATE TABLE ground.airline
(
    id   serial PRIMARY KEY,
    name varchar(120) NOT NULL,
    code char(2)      NOT NULL UNIQUE
);

-- 机票信息
DROP TABLE IF EXISTS ground.ticket;
CREATE TABLE ground.ticket
(
    id            serial PRIMARY KEY,
    dairport_code char(3) REFERENCES ground.airport (code),
    ddate         date,
    dtime         time,
    aairport_code char(3) REFERENCES ground.airport (code),
    adate         date,
    atime         time,
    airline_code  char(2) REFERENCES ground.airline (code),
    aircraft      varchar(20),
    aircraft_type varchar(20),
    price         int4,
    discount      float4,
    class         varchar(20),
    cdate         date
);

-- 供应商
DROP TABLE IF EXISTS ground.provider;
CREATE TABLE ground.provider
(
    id        serial PRIMARY KEY NOT NULL,
    name      varchar(80)        NOT NULL,
    site      varchar(240),
    icon_path varchar(240)
);
