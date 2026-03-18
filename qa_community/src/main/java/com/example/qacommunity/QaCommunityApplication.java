package com.example.qacommunity;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.example.qacommunity.mapper")
public class QaCommunityApplication {

    public static void main(String[] args) {
        SpringApplication.run(QaCommunityApplication.class, args);
    }
}