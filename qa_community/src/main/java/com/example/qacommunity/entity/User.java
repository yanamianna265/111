package com.example.qacommunity.entity;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class User {
    private Integer userId;
    private String username;
    private String passwordHash;
    private String email;
    private LocalDateTime createdAt;
}