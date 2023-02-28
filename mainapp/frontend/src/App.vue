<script setup>
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#"><h1 class="display-6">VGRS</h1></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/Recommendations">Recommendations</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/Quiz">Quiz</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/PlayList">Play List</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/CompletedList">Completed List</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/DislikeList">Dislike List</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/Profile">Profile</router-link>
            </li>
          </ul>
        </div>
      </nav>

    <router-view></router-view>
</template>
