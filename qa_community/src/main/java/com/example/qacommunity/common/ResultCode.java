package com.example.qacommunity.common;

import lombok.Getter;

@Getter
public enum ResultCode {
    SUCCESS(200, "成功"),
    ERROR(500, "服务器内部错误"),
    PARAM_ERROR(400, "参数错误"),
    USER_EXISTS(409, "用户已存在"),
    USER_NOT_FOUND(404, "用户不存在"),
    PASSWORD_ERROR(401, "密码错误");

    private final Integer code;
    private final String message;

    ResultCode(Integer code, String message) {
        this.code = code;
        this.message = message;
    }
}
