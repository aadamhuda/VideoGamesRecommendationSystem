import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import App from './App.vue'
import RecommendationsPage from './components/RecommendationsPage.vue'
import Quiz from './components/Quiz/Question.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/Recommendations', name: 'Recommendations', component: RecommendationsPage},
        {path: '/Quiz', name: 'Quiz', component: Quiz},
    ]
})


createApp(App).use(router).mount('#app')