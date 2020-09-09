/*
Date: 2020-8-13 18:36:12
*/

CREATE DATABASE `demo` DEFAULT CHARACTER SET utf8;

USE `demo`;

SET FOREIGN_KEY_CHECKS=0;


-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `nickname` varchar(64) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  `email` varchar(64) DEFAULT NULL,
  `telephone` varchar(64) DEFAULT NULL,
  `userface` varchar(255) DEFAULT NULL,
  `regTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'farmer', '归海一刀', '$2a$10$VDLqXnk29HEQgzrfAGo.5.SRKNr8xxOCgzov5R.aMazTI18vLnc7a', '1', 'yidao@163.com', '13121218888', '', '1997-5-21 00:00:00');
INSERT INTO `user` VALUES ('2', 'admin', '令狐冲', '$2a$10$VDLqXnk29HEQgzrfAGo.5.SRKNr8xxOCgzov5R.aMazTI18vLnc7a', '1', 'linghu@qq.com', '13121218888', '', '2020-5-21 00:00:00');


-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES ('1', '超级管理员');
INSERT INTO `roles` VALUES ('2', '普通用户');
INSERT INTO `roles` VALUES ('3', '农民');
INSERT INTO `roles` VALUES ('4', '数据管理员');
INSERT INTO `roles` VALUES ('5', '业务管理员');



-- ----------------------------
-- Table structure for roles_user
-- ----------------------------
DROP TABLE IF EXISTS `roles_user`;
CREATE TABLE `roles_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rid` int(11) DEFAULT '2',
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rid` (`rid`),
  KEY `uid` (`uid`),
  CONSTRAINT `roles_user_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `roles` (`id`),
  CONSTRAINT `roles_user_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of roles_user
-- ----------------------------
INSERT INTO `roles_user` VALUES ('1', '3', '1');
INSERT INTO `roles_user` VALUES ('2', '4', '2');



-- ----------------------------
-- Table structure for farmer
-- ----------------------------
DROP TABLE IF EXISTS `farmer`;
CREATE TABLE `farmer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `family_number` int(11) DEFAULT NULL,
  `education_level` varchar(32) DEFAULT NULL,
  `physical_condition` varchar(32) DEFAULT NULL,
  `labor_skill` varchar(32) DEFAULT NULL,
  `poverty_state` varchar(32) DEFAULT NULL,
  `poverty_cause` varchar(32) DEFAULT NULL,
  `income` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uid` (`uid`),
  CONSTRAINT `farmer_ibfk` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of farmer
-- ----------------------------
INSERT INTO `farmer` VALUES ('1', '1', '4', '高中', '健康', '普通劳动力', '一般脱贫户', '缺技术', '10000', '600');


SET FOREIGN_KEY_CHECKS=1;