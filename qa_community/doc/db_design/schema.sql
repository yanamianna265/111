-- 简易问答社区数据库建表脚本
-- 数据库名: qa_community
-- 字符集: utf8mb4 (支持emoji)

CREATE DATABASE IF NOT EXISTS qa_community 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE qa_community;

-- ----------------------------
-- 1. 用户表 (User)
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `user_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希值',
    `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱地址',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_username` (`username`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- 2. 问题表 (Question)
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question` (
    `question_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '问题ID',
    `title` VARCHAR(200) NOT NULL COMMENT '问题标题',
    `content` TEXT NOT NULL COMMENT '问题内容',
    `tag` VARCHAR(50) DEFAULT NULL COMMENT '问题标签(如: Java, Spring)',
    `user_id` INT UNSIGNED NOT NULL COMMENT '作者ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_tag` (`tag`),
    INDEX `idx_created_at` (`created_at` DESC)  -- 按时间倒序查询优化
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='问题表';

-- ----------------------------
-- 3. 回答表 (Answer)
-- ----------------------------
DROP TABLE IF EXISTS `answer`;
CREATE TABLE `answer` (
    `answer_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '回答ID',
    `content` TEXT NOT NULL COMMENT '回答内容',
    `question_id` INT UNSIGNED NOT NULL COMMENT '关联问题ID',
    `user_id` INT UNSIGNED NOT NULL COMMENT '作者ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (`question_id`) REFERENCES `question`(`question_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    INDEX `idx_question_id` (`question_id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_created_at` (`created_at` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='回答表';

-- ----------------------------
-- 4. 评论表 (Comment)
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
    `comment_id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '评论ID',
    `content` TEXT NOT NULL COMMENT '评论内容',
    `answer_id` INT UNSIGNED NOT NULL COMMENT '关联回答ID',
    `user_id` INT UNSIGNED NOT NULL COMMENT '作者ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (`answer_id`) REFERENCES `answer`(`answer_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
    INDEX `idx_answer_id` (`answer_id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_created_at` (`created_at` DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

-- ----------------------------
-- 初始化测试数据
-- ----------------------------

-- 插入测试用户
INSERT INTO `user` (`username`, `password_hash`, `email`) VALUES
('alice', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKwC6Fv9Yf4C5J6G7H8I9J0K1L2M', 'alice@example.com'),
('bob', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKwC6Fv9Yf4C5J6G7H8I9J0K1L2M', 'bob@example.com'),
('charlie', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iKwC6Fv9Yf4C5J6G7H8I9J0K1L2M', 'charlie@example.com');

-- 插入测试问题
INSERT INTO `question` (`title`, `content`, `tag`, `user_id`) VALUES
('Java中如何实现单例模式?', '我想了解Java中几种常见的单例模式实现方式，以及它们的优缺点。', 'Java', 1),
('Spring Boot如何集成MyBatis?', '刚学Spring Boot，想用它连接MySQL数据库，请问如何集成MyBatis?', 'Spring Boot', 2),
('Redis缓存穿透怎么解决?', '最近遇到缓存穿透问题，大量请求打到DB，有什么好的解决方案?', 'Redis', 1);

-- 插入测试回答
INSERT INTO `answer` (`content`, `question_id`, `user_id`) VALUES
('Java单例模式有饿汉式、懒汉式、双重检查锁等方式，推荐使用枚举或静态内部类。', 1, 2),
('可以在pom.xml添加mybatis-spring-boot-starter依赖，然后配置数据源即可。', 2, 3),
('可以用布隆过滤器或者缓存空值来解决缓存穿透问题。', 3, 1);

-- 插入测试评论
INSERT INTO `comment` (`content`, `answer_id`, `user_id`) VALUES
('双重检查锁要注意volatile关键字防止指令重排。', 1, 3),
('感谢分享，我去试试看!', 1, 1);