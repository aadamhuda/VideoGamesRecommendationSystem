<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'


export default defineComponent( {
    created() {
        this.get_id()
        this.get_recs()
    },
    data() {
        return {
            user_id: 0,
            games_list: [],
            success: true,
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
        async get_recs() {
            let response = await fetch("http://localhost:8000/user-recommendations", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.games_list = data.games_list
            this.success = data.success
        }
    },
} )

</script>
<template>
    <div v-for="game in this.games_list">
        <div>
            <p>{{game}}</p>
        </div>
    </div>
</template>