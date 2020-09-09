package com.pascal.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pascal.bean.Farmer;
import com.pascal.bean.RespBean;
import com.pascal.service.FarmerService;
import com.pascal.utils.Util;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

@RestController//包含了ResponseBody注解
@RequestMapping("/farmer")
public class FarmerController {
    @Autowired
    ObjectMapper mapper;

    @Autowired
    FarmerService farmerService;


    @GetMapping("/currentFarmer")
    public RespBean getCurrentFarmer(){
        Long uid = Util.getCurrentUser().getId();
        Farmer farmer = farmerService.getFarmerByUid(uid);
        return RespBean.ok("用户信息查询成功", farmer);
    }

    @PostMapping("/currentFarmer")
    public RespBean updateCurrentFarmer(@RequestBody Farmer farmer) throws IOException {
        String Code_Adress = "127.0.0.1";
        Socket socket = new Socket(Code_Adress,9000);
        OutputStream outputStream = socket.getOutputStream();
        InputStream inputStream = socket.getInputStream();
        byte[] bytes = new byte[1024];
        String text = mapper.writeValueAsString(farmer);
        outputStream.write(text.getBytes());
        int len = inputStream.read(bytes);
        String str = new String(bytes,0,len);
        JsonNode root = mapper.readTree(str);
        farmer.setScore(root.path("score").intValue());
        farmerService.updateFarmerByUid(farmer);
        return RespBean.ok("用户信息修改成功", farmer);
    }

    @GetMapping("/menus")
    public RespBean getFarmerMenus(){
        return RespBean.ok("获取菜单成功");
    }
}
