package com.pascal.bean;


import lombok.Data;

import java.io.Serializable;

@Data
public class Role implements Serializable {
    private Long id;

    private String name;
    public Role(Long id, String name){
        this.id = id;
        this. name = name;
    }
}
