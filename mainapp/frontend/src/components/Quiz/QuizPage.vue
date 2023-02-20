<script>
import { defineComponent } from 'vue'

export default defineComponent( {
    created() {
        this.get_id()
    },
    data() {
        return {
            user_id: "",
        }
    },
    methods : {
        async get_id() {
            let response = await fetch("http://localhost:8000/ses-user", {method: "GET", credentials: "include", mode: "cors", referrerPolicy: "no-referrer" })
            let data = await response.json()
            console.log(data);
            this.user_id = data.user_id
        },
    },
} )

</script>
<template>
    
</template>