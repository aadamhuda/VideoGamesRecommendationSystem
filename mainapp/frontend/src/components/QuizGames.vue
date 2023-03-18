<script>
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_id()
        this.get_quiz_games()
    },
    data() {
        return {
            user_id: 0,
            games_list: [],
            success: true,
            checked_names: [],
            curr_game_limit: 20,
            max_games: false,
            loading: false,
            submitted: false,
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("./ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
            this.submitted = false
        },
        async get_quiz_games() {
            this.loading= true
            let response = await fetch("./get-quiz-games", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.games_list = data.games_list
            this.loading = false
            this.success = data.success
            this.curr_game_limit = 20
            this.max_games = false
            this.submitted = false
        },
        async saveProfile() {
            console.log("saved")
            this.get_id()
            this.submitted = false
            let response = await fetch("./store-profile", {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.user_id,
                    games_choice: this.checked_names,
                })
            })
            let data = await response.json()
            this.success = data.success
            this.submitted = true
        },
        async more_games() {
            if ((this.curr_game_limit + 20) >= this.games_list.length){
                this.max_games = true
            }
            else{
                this.max_games = false
                this.curr_game_limit += 20
            }
        }
    },
} )

</script>
<template>
    <div class="jumbotron">
        <h1 class="display-4  text-light py-1 px-3">Quiz</h1>
        <div class=" text-light px-3">
            <p class="lead">Select a few games from this list to complete your profile development. You can use the 'More Games' button to be given more game suggestions.</p>
            <hr class="my-4 lead">
        </div>
    </div>
    <div style=" max-height: 100vh;" class="py-5 text-left text-light  container align-items-center justify-content-center ">
        <div class="d-flex align-items-center justify-content-center" v-if="this.loading">
            <div class="spinner-border text-light" role="status">
                <span class="sr-only"></span>
            </div>
        </div>
        <div class="row">
            <div class="col-8">
                <form @submit.prevent="this.saveProfile()" class="overflow-auto" style="height:60vh;">
                    <button class="btn btn-outline-light m-2" type="submit">Submit</button>
                    <div v-for="game in this.games_list.slice(0,this.curr_game_limit)">
                        <div>
                            <input class="form-check-input mx-1 my-2" v-model = "checked_names" type="checkbox" :id="game" :name="game" v-bind:value="game">
                            <label class="form-check-label lead">{{game}}</label><br>
                        </div>
                    </div>
                </form>
            </div>
            <div class="col-4">
                <router-link class="nav-link" to="/Quiz"><button class="btn btn-outline-light">Back</button></router-link>
                <button class=" my-2 btn btn-outline-light" @click="more_games()" >More Games</button>
                <p v-if="this.max_games" class="lead text-danger">There are no more games left to load.</p>
                <p v-if="this.submitted" class="lead text-success">Your profile was successfully saved.</p>
            </div>
        </div>
    </div>
</template>