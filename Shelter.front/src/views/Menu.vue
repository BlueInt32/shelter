<template>
  <div id="menu" class="pure-u">
    <div class="pure-menu">
      <a class="pure-menu-heading" href="#">Shelter</a>

      <ul class="pure-menu-list">
        <li class="pure-menu-item">
          <router-link to="/add" class="pure-menu-link">Add</router-link>
        </li>
        <li class="pure-menu-item">
          <router-link to="/" class="pure-menu-link">All elements</router-link>
          <!-- <a href="#" class="pure-menu-link"
                >All elements <span class="email-count">(2)</span></a
              > -->
        </li>
        <li class="pure-menu-item">
          <a href="#" class="pure-menu-link">Manage labels</a>
        </li>
        <!-- <li class="pure-menu-item">
          <a href="#" class="pure-menu-link"
            ><span class="email-label-personal"></span>Personal</a
          >
        </li>
        <li class="pure-menu-item">
          <a href="#" class="pure-menu-link"
            ><span class="email-label-work"></span>Work</a
          >
        </li>
        <li class="pure-menu-item">
          <a href="#" class="pure-menu-link"
            ><span class="email-label-travel"></span>Travel</a
          >
        </li> -->
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
export default class Menu extends Vue {}
</script>

<style></style>
