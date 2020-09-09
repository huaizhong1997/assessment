package com.pascal.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.pascal.bean.RespBean;
import com.pascal.bean.User;
import com.pascal.service.UserService;
import com.pascal.utils.JwtUtil;
import com.pascal.utils.Util;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@RestController//包含了ResponseBody注解
public class UserController {
    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    ObjectMapper mapper;

    @Autowired
    private JwtUtil jwtTokenUtil;
    @Autowired
    UserService userService;


    @RequestMapping("/currentUser")
    public RespBean currentUser(){ return RespBean.ok("用户信息查询成功", Util.getCurrentUser());}



    @RequestMapping(value = "/authenticate", method = RequestMethod.POST)
    public RespBean createAuthenticationToken(@RequestBody User user) throws Exception {
        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(user.getUsername(), user.getPassword())
            );
        }
        catch (BadCredentialsException e) {
            throw new Exception("Incorrect username or password", e);
        }

        final UserDetails userDetails = userService
                .loadUserByUsername(user.getUsername());
        final String jwt = jwtTokenUtil.generateToken(userDetails);
        ObjectNode node = mapper.createObjectNode();
        node.put("token", "Bearer " + jwt);
        return RespBean.ok("登录成功", node);
    }

}