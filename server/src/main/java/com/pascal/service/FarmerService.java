package com.pascal.service;

import com.pascal.bean.Farmer;
import com.pascal.mapper.FarmerMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class FarmerService {
    @Autowired
    FarmerMapper farmerMapper;
    public Farmer getFarmerByUid(Long uid){
        Farmer farmer = farmerMapper.getFarmerByUid(uid);
        return farmer;
    }

    public void updateFarmerByUid(Farmer farmer){
        farmerMapper.updateFarmerByUid(farmer);
    }
}
