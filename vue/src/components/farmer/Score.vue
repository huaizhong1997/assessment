<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>信息管理</el-breadcrumb-item>
            <el-breadcrumb-item>资质评估</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>

            <el-table :data="userlist" border stripe style="width: 100%">
                <el-table-column prop="family_number" label="家庭成员"></el-table-column>
                <el-table-column prop="education_level" label="教育水平"></el-table-column>
                <el-table-column prop="physical_condition" label="身体状况"></el-table-column>
                <el-table-column prop="labor_skill" label="劳动技能"></el-table-column>
                <el-table-column prop="poverty_state" label="当前状态"></el-table-column>
                <el-table-column prop="poverty_cause" label="致贫原因"></el-table-column>
                <el-table-column prop="income" label="年收入"></el-table-column>
                <el-table-column prop="score" label="资质评分"></el-table-column>
                <el-table-column label="操作" align="center">
                    <!-- 编辑用户 -->
                    <template v-slot="scope">
                        <el-button
                                type="primary"
                                icon="el-icon-edit"
                                @click="showEditDialog(scope.$index)"
                                size="mini"
                        ></el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-card>

        <el-dialog
                title="修改资质信息"
                :visible.sync="editDialogVisible"
                width="50%"
        >
            <el-form
                    :model="editUserForm"
                    label-width="70px"
                    class="demo-ruleForm"
            >
                <el-form-item label="家庭成员">
                    <el-input v-model="editUserForm.family_number"></el-input>
                </el-form-item>
                <el-form-item label="教育水平">
                    <el-input v-model="editUserForm.education_level" disabled></el-input>
                </el-form-item>
                <el-form-item label="身体状况">
                    <el-input v-model="editUserForm.physical_condition" disabled></el-input>
                </el-form-item>
                <el-form-item label="年收入">
                    <el-input v-model="editUserForm.income"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editUser">确 定</el-button>
      </span>
        </el-dialog>
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
                const { data: res } = await this.$http.get("farmer/currentFarmer");
                var userList = [];
                userList.push(res.data)
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
