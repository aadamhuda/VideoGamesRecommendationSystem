<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent( {
    created() {
        this.get_questions()
        this.get_id()
    },
    data() {
        return {
            questions: [],
            picked:[],
            user_id: 0,
            success: false
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
        async get_questions() {
            let response = await fetch("http://localhost:8000/get-questions", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.questions = data
        },
        async saveTempProfile() {
            console.log("saved")
            this.get_id()
            let response = await fetch("http://localhost:8000/store-temp-profile", {
                method: 'POST',
                body: JSON.stringify({
                    user_id: this.user_id,
                    picked_items: this.picked,
                })
            })
            let data = await response.json()
            this.success = data.success

        },
    },
} )

</script>
<template>
    <div>
        <p>ur topics: {{ picked }}</p>
        <form @submit.prevent="this.saveTempProfile()">
            <div v-for="question in this.questions">
                <div>
                    <h3>{{question.question_text}}</h3>
                    <input v-model="picked[question.question_id-1]" type="radio" :id="'stronglyAgree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.strongly_agree">
                    <label for="stronglyAgree"> Strongly Agree</label><br>
                    <input v-model="picked[question.question_id-1]" type="radio" :id="'agree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.agree">
                    <label for="agree"> Agree</label><br>
                    <input v-model="picked[question.question_id-1]" type="radio" :id="'neither' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.neither">
                    <label for="neither"> Neither</label><br>
                    <input v-model="picked[question.question_id-1]" type="radio" :id="'disagree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.disagree">
                    <label for="disagree"> Disagree </label><br>
                    <input v-model="picked[question.question_id-1]" type="radio" :id="'stronglyDisagree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.strongly_disagree">
                    <label for="stronglyDisagree"> Strongly Disagree</label><br>
                </div>
            </div>
            <button type="submit">Submit</button>
        </form>

        <p>{{ success }}</p>
        <div v-if="success == true"><router-link class="nav-link" to="/QuizGames"><button>Next</button></router-link></div>
        


    </div>
</template>