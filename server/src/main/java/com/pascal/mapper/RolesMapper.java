package com.pascal.mapper;


import com.pascal.bean.Role;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface RolesMapper {
    List<Role> getRolesByUid(Long uid);
}
