<script>
import { objectToString } from '@vue/shared'
import { defineComponent } from 'vue'
import { useRoute } from 'vue-router'


export default defineComponent( {
    created() {
        this.get_id()
        this.get_profile()
    },
    data() {
        return {
            user_id: "",
            user : [],
            edit: false,
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },

        async get_profile() {
            let response = await fetch("http://localhost:8000/user-profile", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user = data.user
            console.log(data);
        },

        async switch_mode(){
            this.edit = !this.edit
        },
        async update_user(fname, sname, uname, email_address, dob) {
            this.get_id()
            let response = await fetch("http://localhost:8000/user-profile", {
                method: 'PUT',
                body: JSON.stringify({
                    user_id: this.user_id,
                    first_name: this.fname,
                    surname: this.sname,
                    username: this.uname,
                    email: this.email_address,
                    date_of_birth: this.dob,
                })
            })
            let data = await response.json()
            this.success = data.success
            this.switch_mode()
            this.get_profile()

        },
    },
} )

</script>
<template>
    <router-link class="nav-link" to="/Quiz"><button>retake quiz</button></router-link>
    <button @click="switch_mode()">Edit</button>
    <div v-if="this.edit">
        <form @submit.prevent="update_user(uname, email_address, dob)">
            <label>First Name: </label>
            <input class="form-control" type="text" name="firstname" :placeholder="this.user.first_name" v-model="fname">

            <label>Surname: </label>
            <input class="form-control" type="text" name="surname" :placeholder="this.user.last_name" v-model="sname">

            <label>Username: </label>
            <input class="form-control" type="text" name="username" :placeholder="this.user.username" v-model="uname">

            <label>Email: </label>
            <input class="form-control" type="email" name="email" :placeholder="this.user.email" v-model="email_address">

            <label>Date Of Birth: </label>
            <input class="form-control" type="text" name="date_of_birth" v-model="dob" :placeholder="this.user.date_of_birth" onfocus="(this.type='date')"><br>

            <button class="btn btn-primary">Submit</button>
        </form>
    </div>
    <div v-else>
        <p>First Name: {{ user.first_name }}</p>
        <p>Surname: {{ user.last_name }}</p>
        <p>Username: {{ user.username }}</p>
        <p>Email: {{ user.email }}</p>
        <p>Date Of Birth: {{ user.date_of_birth }}</p>
    </div>
    
</template>