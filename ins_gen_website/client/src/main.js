// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'     //导入APP组件
import router from './router'     //从路由目录导入路由
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from "axios"     //导入axios库

Vue.config.productionTip = false
Vue.prototype.$axios = axios     //全局注册，通过this.$axios使用，不用每次使用时都import一下axios

Vue.use(VueRouter)
Vue.use(ElementUI)    //使用elementui

/* eslint-disable no-new */
new Vue({                     //new一个vue的实例
  el: '#app',                 //挂载到index.html的id为app的元素上 
  router,
  components: { App },        //导入的组件
  template: '<App/>'          //模板，会把其中的内容替换到挂载的元素上
})
