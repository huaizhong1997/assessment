package com.pascal.mapper;

import com.pascal.bean.Farmer;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface FarmerMapper {
    Farmer getFarmerByUid(@Param("uid") Long uid);
    void updateFarmerByUid(@Param("farmer") Farmer farmer);
}