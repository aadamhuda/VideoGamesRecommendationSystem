import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import App from './App.vue'
import Home from './components/Home.vue'
import RecommendationsPage from './components/RecommendationsPage.vue'
import Quiz from './components/Question.vue'
import QuizGames from './components/QuizGames.vue'
import PlayList from './components/PlayList.vue'
import CompletedList from './components/CompletedList.vue'
import DislikeList from './components/DislikeList.vue'
import Profile from './components/Profile.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/Home', name: 'Home', component: Home},
        {path: '/Recommendations', name: 'Recommendations', component: RecommendationsPage},
        {path: '/Quiz', name: 'Quiz', component: Quiz},
        {path: '/QuizGames', name: 'QuizGames', component: QuizGames},
        {path: '/PlayList', name: 'PlayList', component: PlayList},
        {path: '/CompletedList', name: 'CompletedList', component: CompletedList},
        {path: '/DislikeList', name: 'DislikeList', component: DislikeList},
        {path: '/Profile', name: 'Profile', component: Profile},
    ]
})


createApp(App).use(router).mount('#app')