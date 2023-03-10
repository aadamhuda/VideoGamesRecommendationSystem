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
            rawg_api_key: '8dace1a7448f4d0eb34054f6cdde584b',
            game_choice: 999,
            curr_game_img_src: [],
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
            this.curr_game_img_src = []
            this.get_game_img()
            this.game_data = data.games
            
        },
        async get_game_img(){
            let response = await fetch("https://api.rawg.io/api/games?key="+this.rawg_api_key+ "&search="+this.curr_game, {method: "GET"})
            let data = await response.json()
            console.log(data);
            for (let i = 0; i < 15; i++) {
                if (this.curr_game === data.results[i].name) {
                    this.game_choice = i
                    break
                }
                else{
                    this.game_choice = 999
                }
            } 
            if (this.game_choice!=999) {
                this.curr_game_img_src = data.results[this.game_choice].short_screenshots
            }
        }
    },
} )

</script>
<template>
    <div class="jumbotron">
        <h1 class="display-4  text-light py-1 px-3">Play List</h1>
        <div class=" text-light px-3">
            <hr class="my-4 lead">
        </div>
    </div>
    <br>
    <div class="container">
        <div v-if="this.games_list.length == 0" class=" py-5 text-left text-light align-items-center justify-content-center text-center h-100 ">
            <p class="lead text-light" >You do not seem to have any games on your Play List. Press the "Like" button in the Recommendations page to add items to this list.</p>
            <p class="lead text-light mx-2">
                <a class="btn btn-outline-light" href="/Recommendations" role="button">Recommendations Page</a>
            </p>
        </div>
        <div class="row">
            <div class="col-4">
                <div class="text-light overflow-auto" style="max-height: 70vh;">
                    <table class="table table-hover">
                        <tbody>
                            <tr v-for="game in games_list" :key="game" @click="get_game_data(game)">
                                <td class="align-middle text-light lead" >{{ game }}</td>
                            </tr>
                        </tbody>
                    </table> 
                </div>
            </div>
            <div class="col-8" v-if="!this.empty">
                <div class="container lead text-light overflow-auto" style="max-height: 70vh;">
                    <h3 >{{ this.game_data.title }}</h3>
                    <div v-if="this.curr_game_img_src.length != 0"><img :src="this.curr_game_img_src[0].image" class=" img-thumbnail" id="gameimg" style="height: 25vh;"></div> 
                    <div class="row ">
                        <div class="col">
                            <p><strong>Genre: </strong>{{ game_data.genre }}</p>
                        </div>
                        <div class="col">
                            <p><strong>Release Date: </strong>{{game_data.release_date }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p><strong>Developer: </strong>{{ game_data.developer }}</p>
                        </div>
                        <div class="col">
                            <p><strong>Number of Players: </strong>{{game_data.num_players }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p><strong>Platforms: </strong>{{ game_data.platforms }}</p>
                        </div>
                        <div class="col">
                            <p><strong>Metascore: </strong>{{game_data.metascore }}</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p><strong>ESRB Rating: </strong>{{ game_data.esrb_rating }}</p>
                        </div>
                        <div class="col">
                            <p><strong>User Score: </strong>{{game_data.userscore }}</p>
                        </div>
                    </div>
                    <p class="lead text-light"><strong>Summary: </strong>{{ game_data.summary }}</p>
                    <div class="btn-group"> 
                        <button class="mx-1 btn btn-outline-success" @click="complete(curr_game)" type="submit">Complete</button>
                        <button class="mx-1 btn btn-outline-warning" @click="dislike_game(curr_game)" type="submit">Dislike</button>
                        <button class="mx-1 btn btn-outline-danger" @click="remove_game(curr_game)" type="submit">Remove</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>