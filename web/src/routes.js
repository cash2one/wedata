import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Main from './views/Main.vue'
import OfficialAccountList from './views/wechat/OfficialAccountList.vue'
import ArticleList from './views/wechat/ArticleList.vue'

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    {
        path: '/',
        component: Home,
        name: 'project',
        displayName: '项目',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            { path: '/accounts', component: OfficialAccountList, displayName: '公众号列表', name: 'OfficialAccountList'},
            { path: '/account/:name', component: ArticleList, displayName: '文章列表', name: 'AritcleList'}
        ]
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;
