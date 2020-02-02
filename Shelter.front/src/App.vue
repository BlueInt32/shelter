<template>
  <div id="layout" class="content pure-g">
    <div id="nav" class="pure-u">
      <a href="#" class="nav-menu-button">Menu</a>
      <div class="nav-inner">
        <!-- <button class="primary-button pure-button">Create</button> -->
        <router-link to="/add" class="primary-button pure-button"
          >Add</router-link
        >

        <div class="pure-menu">
          <ul class="pure-menu-list">
            <li class="pure-menu-item">
              <router-link to="/" class="pure-menu-link"
                >All elements</router-link
              >
              <!-- <a href="#" class="pure-menu-link"
                >All elements <span class="email-count">(2)</span></a
              > -->
            </li>
            <li class="pure-menu-item">
              <a href="#" class="pure-menu-link">Manage labels</a>
            </li>
            <li class="pure-menu-heading">Labels</li>
            <li class="pure-menu-item">
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
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- <div class="pure-menu pure-menu-horizontal">
      <router-link to="/" class="pure-menu-heading pure-menu-link"
        >Shelter</router-link
      >
      <ul class="pure-menu-list">
        <li class="pure-menu-item">
          <router-link to="/add" class="pure-menu-link">Add</router-link>
        </li>
        <li class="pure-menu-item">
          <router-link to="/about" class="pure-menu-link">About</router-link>
        </li>
      </ul>
    </div> -->
    <router-view />
    <vue-snotify></vue-snotify>
  </div>
</template>

<style lang="scss">
@import './styles/custom.scss';
@import 'purecss';
@import '~vue-snotify/styles/simple';
body {
  color: #333;
}
</style>
