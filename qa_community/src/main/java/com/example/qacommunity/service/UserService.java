package com.example.qacommunity.service;

public interface UserService {
    /**
     * 用户注册
     * @param username 用户名
     * @param password 密码
     * @param email 邮箱（可选）
     * @return 注册成功的用户信息
     */
    com.example.qacommunity.entity.User register(String username, String password, String email);

    /**
     * 用户登录
     * @param username 用户名
     * @param password 密码
     * @return JWT token
     */
    String login(String username, String password);
}
