<template>
  <div id="app">
    <vue-snotify></vue-snotify>
    <div class="pure-menu pure-menu-horizontal">
      <a href="#" class="pure-menu-heading pure-menu-link">Shelter</a>
      <ul class="pure-menu-list">
        <li class="pure-menu-item">
          <router-link to="/" class="pure-menu-link">Home</router-link>
        </li>
        <li class="pure-menu-item">
          <router-link to="/about" class="pure-menu-link">About</router-link>
        </li>
        <li class="pure-menu-item">
          <router-link to="/add" class="pure-menu-link">Add</router-link>
        </li>
      </ul>
    </div>
    <router-view />
  </div>
</template>

<style lang="scss">
@import './styles/custom.scss';
@import 'purecss';
body {
  color: #333;
}
</style>
