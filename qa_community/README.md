# 简易问答社区 - 后端项目

## 项目简介
一个类似知乎/Stack Overflow的简易问答社区后端服务，支持用户管理、问题发布、回答、评论等核心功能。

## 技术栈
- Spring Boot 3.2.x
- MyBatis
- MySQL 8.0+
- JWT 认证
- Lombok
- Maven


### 1. 环境准备（Day1）
- JDK 17+
- MySQL 8.0+
- Maven 3.6+

### 2. 初始化数据库(Day1)
mysql -u root -p < ../doc/db_design/schema.sql

### 3. 修改配置文件
编辑 `src/main/resources/application.yml`，修改数据库连接信息：
yaml
spring:
datasource:
url: jdbc:mysql://localhost:3306/qa_community?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true&characterEncoding=utf8
username: your_mysql_username
password: your_mysql_password

### 4.完成接口

### 5. 运行项目
mvn spring-boot:run

### 6. 测试接口
使用 Postman 或 curl 测试：
    注册用户，登录用户功能正常

## 当前进度 (Day 2)2026-3-18
✅ 完成 Spring Boot 项目初始化  
✅ 完成数据库配置  
✅ 实现用户实体与 Mapper  
✅ 实现统一响应格式与全局异常处理  
✅ 实现用户注册接口（含参数校验、密码加密）  
✅ 实现用户登录接口（JWT 认证）  
✅ 完成接口测试

## 2026-3-19
DAY 3
任务清单：实现核心业务CRUD
1.问题部分
（1）.发布问题（带标签）
（2）.分页查询问题列表（时间排序）
（3）.查看详细问题
2.回答部分
（1）针对问题发布回答
（2）查询所有回答
3.测试