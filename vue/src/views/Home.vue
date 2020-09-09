<template>
  <el-container style="height:100vh">
    <el-header>
      <div>
        <img src="../assets/logo.png" alt />
        <span>资质评估系统</span>
      </div>
      <el-button type="info" @click="logout">退出</el-button>
    </el-header>
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <el-menu
          router
          background-color="#333744"
          text-color="#fff"
          active-text-color="#409EFF"
          unique-opened
          :collapse="isCollapse"
          :collapse-transition="false"
          :default-active="$route.path"
        >
          <el-submenu :index="item.id+''" v-for="item in menulist" :key="item.id">
            <template slot="title">
              <i :class="iconObj[item.id]"></i>
              <span>{{item.authName}}</span>
            </template>
            <el-menu-item :index="'/'+subItem.path" v-for="subItem in item.children" :key="subItem.id">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span>{{subItem.authName}}</span>
              </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      menulist: [],
      farmerMenulist: [
        {"id":3,"authName":"信息管理","path":"scores","children":[{"id":103,"authName":"个人信息","path":"farmers","children":[],"order":null}, {"id":104,"authName":"资质评估","path":"scores","children":[],"order":null}],"order":1},
        {"id":2,"authName":"数据统计","path":"reports","children":[{"id":102,"authName":"数据报表","path":"reports","children":[],"order":null}],"order":2}
      ],
      administartorMenulist: [
        {"id":0,"authName":"用户管理","path":"users","children":[{"id":100,"authName":"用户列表","path":"users","children":[],"order":null}],"order":1},
        {"id":1,"authName":"模型管理","path":"models","children":[{"id":101,"authName":"模型参数","path":"models","children":[],"order":null}],"order":2},
        {"id":2,"authName":"数据统计","path":"reports","children":[{"id":102,"authName":"数据报表","path":"reports","children":[],"order":null}],"order":3}
      ],
      iconObj: {
        "125": "iconfont icon-icon_user",
        "103": "iconfont icon-tijikongjian",
        "101": "iconfont icon-shangpin",
        "102": "iconfont icon-danju",
        "145": "iconfont icon-baobiao"
      },
      isCollapse: false,
    };
  },
  methods: {
    logout() {
      window.sessionStorage.clear;
      this.$router.push("/login");
    },
    async getMenuList() {

      const { data:res } = await this.$http.get("currentUser");
      if (res.status === 200) {
        var role = res.data.roles[0].name;
        if(role == "农民"){
          this.menulist = this.farmerMenulist;
        }
        else if(role == "数据管理员") {
          this.menulist = this.administartorMenulist;
        }
      } else {
        this.$message({
          type: "error",
          message: res.msg
        });
      }
    },
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    }
  },
  created() {
    this.getMenuList();
  }
};
</script>

<style lang="less" scoped>
.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #fff;
  font-size: 20px;
  > div {
    display: flex;
    align-items: center;
    span {
      margin-left: 15px;
    }
  }
  img {
    width: 50px;
    height: 50px;
  }
}

.el-aside {
  background-color: #333744;
  .el-menu {
    border-right: none;
  }
}

.el-main {
  background-color: #eaedf1;
}

.iconfont {
  margin-right: 10px;
}

.toggle-button {
  background-color: #4a5064;
  font-size: 10px;
  line-height: 24px;
  color: #fff;
  text-align: center;
  letter-spacing: 0.2em;
  cursor: pointer;
}
</style>