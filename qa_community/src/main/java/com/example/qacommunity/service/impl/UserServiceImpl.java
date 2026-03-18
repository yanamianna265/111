package com.example.qacommunity.service.impl;

import com.example.qacommunity.entity.User;
import com.example.qacommunity.exception.BusinessException;
import com.example.qacommunity.mapper.UserMapper;
import com.example.qacommunity.service.UserService;
import com.example.qacommunity.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private JwtUtil jwtUtil;

    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User register(String username, String password, String email) {
        // 检查用户名是否已存在
        User existingUser = userMapper.selectByUsername(username);
        if (existingUser != null) {
            throw new BusinessException("用户名已存在");
        }

        // 密码加密
        String encodedPassword = passwordEncoder.encode(password);

        // 创建用户对象
        User user = new User();
        user.setUsername(username);
        user.setPasswordHash(encodedPassword);
        user.setEmail(email);
        user.setCreatedAt(LocalDateTime.now());

        // 插入数据库
        userMapper.insert(user);

        // 清除密码后返回
        user.setPasswordHash(null);
        return user;
    }

    @Override
    public String login(String username, String password) {
        // 查找用户
        User user = userMapper.selectByUsername(username);
        if (user == null) {
            throw new BusinessException("用户名或密码错误");
        }

        // 验证密码
        if (!passwordEncoder.matches(password, user.getPasswordHash())) {
            throw new BusinessException("用户名或密码错误");
        }

        // 生成 JWT token
        return jwtUtil.generateToken(user.getUserId(), user.getUsername());
    }
}