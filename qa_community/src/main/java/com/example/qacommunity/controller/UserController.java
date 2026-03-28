package com.example.qacommunity.controller;

import com.example.qacommunity.common.Result;
import com.example.qacommunity.entity.User;
import com.example.qacommunity.service.UserService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/user")
@Validated
public class UserController {

    @Autowired
    private UserService userService;

    /**
     * 用户注册
     * POST /api/user/register
     */
    @PostMapping("/register")
    public Result<User> register(
            @RequestParam @NotBlank(message = "用户名不能为空")
            @Size(min = 3, max = 20, message = "用户名长度必须在3-20之间")
            String username,

            @RequestParam @NotBlank(message = "密码不能为空")
            @Size(min = 6, max = 20, message = "密码长度必须在6-20之间")
            String password,

            @RequestParam(required = false)
            @Email(message = "邮箱格式不正确")
            String email) {

        User user = userService.register(username, password, email);
        return Result.success(user);
    }

    /**
     * 用户登录
     * POST /api/user/login
     */
    @PostMapping("/login")
    public Result<String> login(
            @RequestParam @NotBlank(message = "用户名不能为空") String username,
            @RequestParam @NotBlank(message = "密码不能为空") String password) {

        String token = userService.login(username, password);
        return Result.success(token);
    }

    /**
     * 获取当前用户信息（需要登录）
     * GET /api/user/info
     */
    @GetMapping("/info")
    public Result<User> getUserInfo(
            @RequestHeader("Authorization") String token) {
        // 验证 token 并获取用户信息
        // 这里先简单返回成功，后续添加 token 验证逻辑
        return Result.success(null);
    }
}