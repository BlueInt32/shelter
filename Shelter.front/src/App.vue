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
    <router-view class="pure-g" :class="{ active: !menuModule.isMenuOpen }" />
    <vue-snotify />
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import MenuModule from '@/store/menu';
import Menu from '@/views/Menu.vue';

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
