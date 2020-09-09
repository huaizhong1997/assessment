<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>模型管理</el-breadcrumb-item>
            <el-breadcrumb-item>模型参数</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card align="center">
            <el-button type="primary" @click="train" :center=true :loading="loading">{{text}}</el-button>
        </el-card>

    </div>
</template>

<script>
    export default {
        data() {
            return {
                loading: false,
                text: "开始训练",
            };
        },
        methods: {
            async train() {
                this.loading = true;
                this.text = "模型训练中";
                const { data: res } = await this.$http.post("administrator/model");
                if (res.status==200){
                    this.$message({
                        message:'模型训练成功',
                        type:'success'
                    })
                    this.loading = false;
                    this.text = "开始训练"
                }else {
                    this.$message({
                        message: res.msg,
                        type: 'error'
                    })
                }

            }
        },
        created() {
        }
    };
</script>

<style lang="less" scoped></style>
