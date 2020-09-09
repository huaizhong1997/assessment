package com.pascal.bean;

import lombok.Data;

import java.io.Serializable;

@Data
public class Farmer implements Serializable {
    private Long id;
    private Long uid;
    private String family_number;
    private String education_level;
    private String physical_condition;
    private String labor_skill;
    private String poverty_state;
    private String poverty_cause;
    private Integer income;
    private Integer score;
}