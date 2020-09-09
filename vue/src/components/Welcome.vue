<template>
  <div>
    <h3>Hello，{{username}}</h3>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
    };
  },
  async created() {
    const { data:res } = await this.$http.get("currentUser");
    if (res.status === 200) {
      this.username = res.data.nickname;
    }
    else{
      this.$message({
        type: "error",
        message: res.msg
      });
    }
  }
}
</script>

<style lang="less" scoped>

</style>