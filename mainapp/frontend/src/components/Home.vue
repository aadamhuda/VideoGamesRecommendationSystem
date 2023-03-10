<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'


export default defineComponent( {
    created() {
        this.get_id()
        this.get_home_data()
        this.get_recs()
    },
    data() {
        return {
            user_id: 0,
            games_list: [],
            success: true,
            top_genre: '',
            completed_overview: [],
            play_overview: [],
            loading: false,
            user_name: ''
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
        async get_home_data() {
            let response = await fetch("http://localhost:8000/home-page", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.top_genre = data.top_genre
            this.completed_overview = data.completed_overview
            this.play_overview = data.play_overview
            this.user_name = data.user_name
        },
        async get_recs() {
            this.games_list = []
            this.loading = true
            let response = await fetch("http://localhost:8000/user-recommendations", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.loading = false
            this.games_list = data.games_list
            this.success = data.success
        },
    },
} )

</script>
<template>
    <div class=" text-light">
        <div class="jumbotron px-5">
            <h1 class="display-4  text-light">Hello {{ user_name }}!</h1>
            <div v-if="this.top_genre == ''" class=" p-5 text-left text-light container d-flex align-items-center justify-content-center text-center h-100 ">
                <p class="lead text-light" >You do not seem to have any genres registered, please take the quiz to begin your profile! </p>
                <p class="lead text-light mx-2">
                    <a class="btn btn-outline-light" href="/Quiz" role="button">Take Quiz</a>
                </p>
            </div>
            <p v-else class="lead  text-light">Nice! Your favourite genre seems to be {{ top_genre }}. Happy gaming! </p>
        </div>
        <div v-if="this.top_genre != ''" class="container p-5 text-left text-light container d-flex align-items-center justify-content-center text-center h-75 ">
            <div class="row">
                <div class="col px-5">
                    <div>
                        <h5 class="lead " ><strong>Recommendations Overview</strong></h5>
                        <p class="lead">Here is a glance at a few games you might like:</p>
                        <div class="h-100 d-flex align-items-center justify-content-center py-5" v-if="this.loading">
                            <div class="spinner-border text-light" role="status">
                                <span class="sr-only"></span>
                            </div>
                        </div>
                        <table class="table  text-light">
                            <tbody>
                                <tr v-for="game in games_list.slice(0,5)">
                                    <td class="align-middle d-flex align-items-center justify-content-center  lead" >{{ game }}</td>
                                </tr>
                            </tbody>
                        </table> 
                    </div>
                </div>
                <div class="col px-5">
                    <h5 class="lead"><strong>Play List Overview</strong></h5>
                    <p class="lead">Here are some of the games that you have added to your play list:</p>
                    <table class="table text-light">
                        <tbody>
                            <tr v-for="game in play_overview">
                                <td class="align-middle  d-flex align-items-center justify-content-center lead" >{{ game }}</td>
                            </tr>
                        </tbody>
                    </table> 
                </div>
                <div class="col px-5">
                    <h5 class="lead" ><strong>Completed Games Overview</strong></h5>
                    <p class="lead">Here are some games you have completed:</p>
                    <table class="table  text-light">
                        <tbody>
                            <tr v-for="game in completed_overview">
                                <td class="align-middle  d-flex align-items-center justify-content-center lead" >{{ game }}</td>
                            </tr>
                        </tbody>
                    </table> 
                </div>
            </div>
        </div>
    </div>
</template>