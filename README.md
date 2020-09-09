一、部署流程

1、vue

```
npm run build
```

2、java

```
cd target
java -jar server.jar
```

3、python

4、目录结构

```
assess                         
    ├── server.jar
    ├── main.py  
    ├── dist   
    │   ├── index.html
    │   ├── css     
    │   ├── js
    │   └── img
    │   └── fonts
    ├── data                     
    │   ├── poor.csv
    │   ├── param_cut.csv
    │   ├── param_score.csv
    ├── log                   
    │   ├── java.log
    │   └── python.log
```

5、启动服务器

```
nohup java -jar server.jar >log/java.log &

nohup python -u main.py >log/python.log &
```

6、公网地址

```
http://60.205.226.163:8080/
```

二、功能介绍

农户：查看个人信息、修改个人信息并重新评估

```
username：farmer
password：123456
```

管理员：更新模型

```
username：admin
password：123456
```

