<template>
  <div
    id="layout"
    class="content"
    :class="{ active: menuModule.isMenuOpen, closed: !menuModule.isMenuOpen }"
  >
    <a
      href="#"
      id="menuLink"
      class="menu-link"
      :class="{ active: menuModule.isMenuOpen }"
      @click="menuLinkClickHandler"
    >
      <span></span>
    </a>
    <Menu :isMenuOpen="menuModule.isMenuOpen" />
    <router-view
      class="pure-g page-content"
      :class="{ active: !menuModule.isMenuOpen }"
    />
    <vue-snotify />
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import MenuModule from '@/store/menu';
import Menu from '@/views/Menu.vue';

// font-awesome dependencies
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCircleNotch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faCircleNotch);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.filter('capitalize', function(value: string) {
  if (!value) return '';
  value = value.toString();
  return value.charAt(0).toUpperCase() + value.slice(1);
});
@Component({
  components: {
    Menu
  }
})
export default class App extends Vue {
  private menuLinkOpen: boolean = false;
  private menuModule = getModule(MenuModule);

  public menuLinkClickHandler() {
    this.menuModule.setMenuOpenState(!this.menuModule.isMenuOpen);
  }
}
</script>
<style lang="scss">
@import './styles/custom.scss';
@import 'purecss';
@import '~vue-snotify/styles/simple';
body {
  color: #333;
}
</style>
