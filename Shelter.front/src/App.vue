<template>
  <div id="layout" class="content pure-g">
    <!-- <a href="#menu" id="menuLink" class="menu-link pure-u">
      <span></span>
    </a> -->
    <Menu />
    <router-view />
    <vue-snotify />
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import Menu from '@/views/Menu.vue';

@Component({
  components: {
    Menu
  }
})
export default class App extends Vue {}
</script>
<style lang="scss">
@import './styles/custom.scss';
@import 'purecss';
@import '~vue-snotify/styles/simple';
body {
  color: #333;
}
</style>
