package com.pascal;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
@SpringBootTest
class BlogApplicationTests {

    @Test
    void contextLoads() {
        Socket socket = null;
        String Code_Adress = "127.0.0.1";
        try {
            socket = new Socket(Code_Adress,9007);
            OutputStream outputStream = socket.getOutputStream();
            InputStream inputStream = socket.getInputStream();
            byte[] bytes = new byte[1024];
            outputStream.write("我是JAVA客户端".getBytes());
            int len = inputStream.read(bytes);
            String str = new String(bytes,0,len);
            System.out.println(str);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
