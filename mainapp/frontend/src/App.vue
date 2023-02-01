<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#"><h1 class="display-6">Auction App</h1></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/view_items">All Items</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/Profile">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/my_items">My Items</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/auctionForm">Post an Item</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="http://localhost:8000/logout" >Logout</a>
            </li>
          </ul>
        </div>
      </nav>

    <router-view></router-view>
</template>
