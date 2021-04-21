# 机票元搜索及智能推荐系统<br>Ticket Meta Search and Recommendation System

## 1. 机票数据爬虫（crawler）

### 1.1 已有数据

北京->昆明 2019年 出发前45天 每天 某航班 最低价

### 1.2 数据/爬虫需求

- 离线数据爬取：每天主要城市数据
- 实时爬虫

准备爬取的数据：8个大城市之间航班，48天价格变化

### 1.3 遇到的问题

- 数据太多
- 反爬机制
- 爬取太慢

### 1.3 所用技术

- ip池
- 多线程：Python多线程技术，并发请求数据，线程互斥写文件

## 2. 数据处理模块（data)

### 2.1 数据清洗

2019 昆明至北京数据处理

### 2.2 数据导入

Shell脚本导入 HDFS

## 3. 机器学习模块（spark）

### 3.1 价格预测

模型选择：Regression Tree
神经网络算法，树形算法，决策树，回归决策树

可选features
- 出发日期
- 航空公司
- 一周第几天
- 是否节假日
- 距出发日多少天
- 原价（折扣）

### 3.2 何时买

## 4. 后端（backend）

框架：Python Flask
数据库：PostgreSQL

### 4.1 RESTful API 设计

- `/airlines`
- `/sites`
- `/tickets?date=2021-4-30&source=BJS&destination=CKG&sort=**`
- `/users/<userid>` overview
- `/users/<userid>?tab=**` tab: marks, 
- `/cities` 城市列表
- `/cities/<citiid>` 城市推荐目的地及价格、日期

### 4.2 数据库设计

机场
城市
航空公司
航班
机票
供应商

## 5. 前端（frontend）

框架：Vue

## 5.1 主页

搜索框+导航

## 5.2 查询页

条件查询
列表

## 5.3 价格趋势

价格变化图

## 5.4 飞去哪

地图
