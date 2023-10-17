<template>
  <div id="app">
    <router-view />
    <!-- 显示路由组件 -->
  </div>
</template>

<script>
export default {    //导出组件，main.js中才能导入
  name: "App",
};
</script>

<style>
@import "./fonts/font.css";    

#app {
  font-family: "Times New Roman", "华文中宋", "楷体";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
