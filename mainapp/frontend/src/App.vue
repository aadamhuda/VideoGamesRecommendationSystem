<script setup>
</script>

<template>
  <div class="bg-image shadow-2-strong" style="background-image: url('https://wallpaperaccess.com/full/906751.jpg'); height: 100vh" id="bgimg">
      <div class="mask" style="background-color: rgba(0, 0, 0, 0.65); height: 100vh">
        <nav class="navbar navbar-expand-lg navbar-light text-light">
          <router-link class="nav-link" to="/Home"><h1 class="display-6 p-2">VGRS</h1></router-link>
            <div class="collapse navbar-collapse">
              <ul class="navbar-nav">
                  <li class="nav-item lead">
                    <router-link class="nav-link mx-1 text-light" to="/Home">Home</router-link>
                  </li>
                  <li class="nav-item lead">
                    <router-link class="nav-link mx-1 text-light" to="/Recommendations">Recommendations</router-link>
                  </li>
                  <li class="nav-item lead">
                    <router-link class="nav-link mx-1 text-light" to="/PlayList">Play List</router-link>
                  </li>
                  <li class="nav-item lead">
                    <router-link class="nav-link mx-1 text-light" to="/CompletedList">Completed List</router-link>
                  </li>
                  <li class="nav-item lead">
                    <router-link class="nav-link mx-1 text-light" to="/DislikeList">Dislike List</router-link>
                  </li>
                  <li class="nav-item lead">
                    <router-link class="nav-link mx-1 text-light" to="/Profile">Profile</router-link>
                  </li>
                  <li class="nav-item lead">
                    <a class="nav-link mx-1 text-light" href="http://localhost:8000/logout" >Logout</a>
                  </li>
                </ul>
              </div>
            </nav>
          <router-view></router-view>
      </div>
  </div>
</template>
