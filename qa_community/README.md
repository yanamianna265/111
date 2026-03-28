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
 使用Apifox进行测试：
    （1）注册用户，登录用户功能正常
    参数：username、password、email（可选）
    新建请求 → 选择 POST
    输入 URL: http://localhost:8080/api/user/register
    添加参数：
    username: alice123
    password: 123456
    email: alice123@example.com
    （注册成功）

    （2）登录接口正常
    新建请求 → 选择 POST
    输入 URL: http://localhost:8080/api/user/login
    添加参数：
    username: alice123
    password: 123456
    （登录成功）

## 当前进度 (Day 2)
✅ 完成 Spring Boot 项目初始化  
✅ 完成数据库配置  
✅ 实现用户实体与 Mapper  
✅ 实现统一响应格式与全局异常处理  
✅ 实现用户注册接口（含参数校验、密码加密）  
✅ 实现用户登录接口（JWT 认证）  
✅ 完成接口测试