<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>信息管理</el-breadcrumb-item>
            <el-breadcrumb-item>个人信息</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>

            <el-table :data="userlist" border stripe style="width: 100%">
                <el-table-column prop="username" label="用户名"></el-table-column>
                <el-table-column prop="nickname" label="姓名"></el-table-column>
                <el-table-column prop="email" label="邮箱"></el-table-column>
                <el-table-column prop="telephone" label="手机"></el-table-column>
                <el-table-column prop="role" label="角色"></el-table-column>
            </el-table>
        </el-card>

    </div>
</template>

<script>
    export default {
        data() {
            return {
                dialogVisible: false,
                editDialogVisible: false,
                editUserForm: '',
                userlist: [],
            };
        },
        methods: {
            async getUserList() {
                const { data: res } = await this.$http.get("currentUser");
                var userList = [];
                userList.push(res.data)
                userList[0].role = userList[0].roles[0].name;
                this.userlist = userList;
            },
            async showEditDialog(index) {
                this.editUserForm = this.userlist[index];
                this.editDialogVisible = true;
            },
            async editUser() {
                const { data: res } = await this.$http.post("farmer/currentFarmer", this.editUserForm);
                if (res.status==200){
                    this.$message({
                        message:'修改成功',
                        type:'success'
                    })
                    this.getUserList();
                }else {
                    this.$message({
                        message: res.msg,
                        type: 'error'
                    })
                }
                this.editDialogVisible = false;

            }
        },
        created() {
            this.getUserList();
        }
    };
</script>

<style lang="less" scoped></style>
