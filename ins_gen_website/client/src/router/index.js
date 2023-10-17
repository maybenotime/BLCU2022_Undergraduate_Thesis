import Vue from 'vue'
import Router from 'vue-router'
import Mainpage from '../components/Mainpage'   //导入Mainpage组件

Vue.use(Router)             //使用Router

export default new Router({             //导出路由
    routes:[
        {                           
            path: '/',
            name: 'Mainpage',
            component: Mainpage
        }           
    ]

})

