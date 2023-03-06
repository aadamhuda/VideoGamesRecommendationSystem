<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'


export default defineComponent( {
    created() {
        this.get_id()
        this.get_play_list()
    },
    data() {
        return {
            user_id: 0,
            games_list: [],
            success: true,
            curr_game: '',
            game_data: [],
            empty: true,
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
        async complete(game) {
            this.remove_game(game)
            this.complete_game(game)
        },
        async dislike(game) {
            this.remove_game(game)
            this.dislike_game(game)
        },

        async complete_game(completed) {
            this.get_id()
            let response = await fetch("http://localhost:8000/completed-game", {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.user_id,
                    completed_game: completed,
                })
            })
            let data = await response.json()
            this.success = data.success
            this.get_play_list()

        },
        async dislike_game(disliked) {
            this.get_id()
            let response = await fetch("http://localhost:8000/dislike-game", {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.user_id,
                    disliked_game: disliked,
                })
            })
            let data = await response.json()
            this.success = data.success
            this.get_play_list()

        },
        async remove_game(game) {
            this.get_id()
            let response = await fetch("http://localhost:8000/remove-list-game", {
                method: 'DELETE',
                body: JSON.stringify({
                    user_id: this.user_id,
                    game_to_remove: game,
                    curr_list: 'liked'
                })
            })
            let data = await response.json()
            this.success = data.success
            this.get_play_list()

        },
        async get_play_list() {
            let response = await fetch("http://localhost:8000/get-user-liked", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.games_list = data.games_list
            this.success = data.success
            this.empty = true
            this.curr_game = ''
        },
        async get_game_data(game){
            this.curr_game = game
            this.empty = false
            let response = await fetch("http://localhost:8000/get-game-data/" + this.curr_game, {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.game_data = data.games
        }
    },
} )

</script>
<template>
    <div class="container">
        <div class="row">
            <div class="col-4">
                <table class="table table-hover">
                    <tbody>
                        <tr v-for="game in games_list" :key="game" @click="get_game_data(game)">
                            <td class="align-middle" >{{ game }}</td>
                        </tr>
                    </tbody>
                </table> 
            </div>
            <div class="col-8" v-if="!this.empty">
                <h3>{{ this.game_data.title }}</h3>
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <p>Genre: {{ game_data.genre }}</p>
                        </div>
                        <div class="col">
                            <p>Release Date: {{game_data.release_date }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p>Developer: {{ game_data.developer }}</p>
                        </div>
                        <div class="col">
                            <p>Number of Players: {{game_data.num_players }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p>Platforms: {{ game_data.platforms }}</p>
                        </div>
                        <div class="col">
                            <p>Metascore: {{game_data.metascore }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p>ESRB Rating: {{ game_data.esrb_rating }}</p>
                        </div>
                        <div class="col">
                            <p>User Score: {{game_data.userscore }}</p>
                        </div>
                    </div>
                    <p>Summary:{{ game_data.summary }}</p>
                </div>
                <form @submit.prevent="complete(curr_game)"><button type="submit">complete</button></form>
                <form @submit.prevent="dislike(curr_game)"><button type="submit">dislike</button></form>
                <form @submit.prevent="remove_game(curr_game)"><button type="submit">remove</button></form>
            </div>
        </div>
    </div>
</template>