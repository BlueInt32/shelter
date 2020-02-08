<template>
  <div id="menu" class="pure-u" :class="{ active: isMenuOpen }">
    <div class="pure-menu">
      <router-link class="pure-menu-heading" to="/">Shelter</router-link>

      <ul class="pure-menu-list">
        <li class="pure-menu-item">
          <router-link to="/add" class="pure-menu-link">Add</router-link>
        </li>
        <li class="pure-menu-item">
          <router-link to="/about" class="pure-menu-link">About</router-link>
          <!-- <a href="#" class="pure-menu-link"
                >All elements <span class="email-count">(2)</span></a
              > -->
        </li>
        <li class="pure-menu-item">
          <a href="#" class="pure-menu-link">Manage labels</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
@Component({})
export default class Menu extends Vue {
  @Prop(Boolean) public isMenuOpen: boolean = false;
}
</script>

<style></style>
