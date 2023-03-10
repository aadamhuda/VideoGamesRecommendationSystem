<script>
import { defineComponent } from 'vue'

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
            let response = await fetch("./ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },

        async get_profile() {
            let response = await fetch("./user-profile", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            this.user = data.user
            console.log(data);
        },

        async switch_mode(){
            this.edit = !this.edit
        },
        async update_user(fname, sname, uname, email_address, dob) {
            this.get_id()
            let response = await fetch("./user-profile", {
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
    <div class="jumbotron">
        <h1 class="display-4  text-light py-1 px-3">Your Profile</h1>
        <div class=" text-light px-3">
            <hr class="my-4 lead">
        </div>
    </div>
    <br>
    <div class="text-left lead text-light container d-flex align-items-center justify-content-center  h-50 ">
        <div class="row w-50">
            <div class="col ">
                <div v-if="this.edit" >
                    <form @submit.prevent="update_user(uname, email_address, dob)">
                        <label class="form-label lead"><strong>First Name: </strong></label>
                        <input class="form-control" type="text" name="firstname" :placeholder="this.user.first_name" v-model="fname">
                        <label class="form-label lead"><strong>Surname: </strong></label>
                        <input class="form-control" type="text" name="surname" :placeholder="this.user.last_name" v-model="sname">
                        <label class="form-label lead"><strong>Username: </strong></label>
                        <input class="form-control" type="text" name="username" :placeholder="this.user.username" v-model="uname">
                        <label class="form-label lead"><strong>Email: </strong></label>
                        <input class="form-control" type="email" name="email" :placeholder="this.user.email" v-model="email_address">
                        <label class="form-label lead"><strong>Date Of Birth: </strong></label>
                        <input class="form-control" type="text" name="date_of_birth" v-model="dob" :placeholder="this.user.date_of_birth" onfocus="(this.type='date')"><br>
                        <button class="btn btn-outline-light">Submit</button>
                    </form>
                </div>
                <div v-else>
                    <p>First Name: {{ user.first_name }}</p>
                    <p>Surname: {{ user.last_name }}</p>
                    <p>Username: {{ user.username }}</p>
                    <p>Email: {{ user.email }}</p>
                    <p>Date Of Birth: {{ user.date_of_birth }}</p>
                </div>
            </div>
            <div class="col d-flex align-items-center justify-content-center">
                <router-link class="nav-link" to="/Quiz"><button class="btn btn-outline-light">Retake quiz</button></router-link>
                <button @click="switch_mode()" class="btn btn-outline-light mx-2">Edit</button>
            </div>
        </div>
    </div>
    
    
</template>