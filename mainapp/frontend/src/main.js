import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import App from './App.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [

    ]
})


createApp(App).use(router).mount('#app')