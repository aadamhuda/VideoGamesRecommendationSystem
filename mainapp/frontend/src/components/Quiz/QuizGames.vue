<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'


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
            checked_names: []
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
        async get_quiz_games() {
            let response = await fetch("http://localhost:8000/get-quiz-games", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.games_list = data.games_list
            this.success = data.success
        },
        async saveProfile() {
            console.log("saved")
            this.get_id()
            let response = await fetch("http://localhost:8000/store-profile", {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.user_id,
                    games_choice: this.checked_names,
                })
            })
            let data = await response.json()
            this.success = data.success

        },
    },
} )

</script>
<template>
    <router-link class="nav-link" to="/Quiz"><button>Back</button></router-link>
    <p>{{ checked_names }}</p>
    <form @submit.prevent="this.saveProfile()">
        <div v-for="game in this.games_list">
            <div>
                <p>{{game}}</p>
                <input v-model = "checked_names" type="checkbox" :id="game" :name="game" v-bind:value="game"><br>
            </div>
        </div>
        <button type="submit">Submit</button>
    </form>
</template>