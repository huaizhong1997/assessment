package com.pascal.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pascal.bean.RespBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

@RestController
@RequestMapping("/administrator")
public class AdministratorController {
    @Autowired
    ObjectMapper mapper;

    @PostMapping("/model")
    public RespBean train() throws IOException {
        String Code_Adress = "127.0.0.1";
        Socket socket = new Socket(Code_Adress,9000);
        OutputStream outputStream = socket.getOutputStream();
        InputStream inputStream = socket.getInputStream();
        byte[] bytes = new byte[1024];
        String text = "Train";
        System.out.println(text);
        outputStream.write(text.getBytes());
        int len = inputStream.read(bytes);
        String str = new String(bytes,0,len);
        JsonNode root = mapper.readTree(str);
        System.out.println(root.path("msg").textValue());
        return RespBean.ok("模型训练成功");
    }
}
