<script>
import { defineComponent } from 'vue'

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
            let response = await fetch("./ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user_id = data.user_id
        },
        async get_questions() {
            let response = await fetch("./get-questions", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.questions = data
        },
        async saveTempProfile() {
            this.get_id()
            let response = await fetch("./store-temp-profile", {
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
    <div class="jumbotron">
        <h1 class="display-4  text-light py-1 px-3">Quiz</h1>
        <div class=" text-light px-3">
            <p class="lead">This Quiz will allow you to initalise your player profile. You must answer at least one question to continue. </p>
            <hr class="my-4 lead">
            <p class=" lead text-warning">WARNING: Answering this quiz will reset your current profile.</p>
        </div>
    </div>
    <div style=" max-height: 100vh;" class="py-3 text-left text-light  container align-items-center justify-content-center ">
        <div class="row">
            <div class="col-8">
                <form @submit.prevent="this.saveTempProfile()" class="overflow-auto" style="height:60vh;">
                    <div v-for="question in this.questions"  >
                        <div>
                            <h3 class="lead"><strong>{{question.question_text}}</strong></h3>
                            <input  class="form-check-input my-2"  v-model="picked[question.question_id-1]" type="radio" :id="'stronglyAgree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.strongly_agree">
                            <label  class="form-check-label lead px-1"  for="stronglyAgree"> Strongly Agree</label><br>
                            <input  class="form-check-input  my-2"  v-model="picked[question.question_id-1]" type="radio" :id="'agree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.agree">
                            <label  class="form-check-label lead px-1"  for="agree"> Agree</label><br>
                            <input  class="form-check-input  my-2"  v-model="picked[question.question_id-1]" type="radio" :id="'neither' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.neither">
                            <label  class="form-check-label lead px-1"  for="neither"> Neither</label><br>
                            <input  class="form-check-input  my-2"  v-model="picked[question.question_id-1]" type="radio" :id="'disagree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.disagree">
                            <label  class="form-check-label lead px-1" for="disagree"> Disagree </label><br>
                            <input  class="form-check-input  my-2"  v-model="picked[question.question_id-1]" type="radio" :id="'stronglyDisagree' + question.question_id" :name="'question' + question.question_id" v-bind:value="question.strongly_disagree">
                            <label  class="form-check-label lead px-1"  for="stronglyDisagree"> Strongly Disagree</label><br>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-outline-light m-2 mx-3">Submit</button>
                </form>
            </div>
            <div class="col-4">
                <div v-if="success == true"><router-link class="nav-link" to="/QuizGames"><button class="btn btn-outline-light">Next</button></router-link></div>
            </div>
        </div>
    </div>
</template>