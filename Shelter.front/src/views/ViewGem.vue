<template>
  <div class="viewGem">
    <h1>{{ gem.title }}</h1>
    <h2>{{ gem.text }}</h2>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import GemsDisplayModule from '@/store/gemsDisplay';
import { Gem } from '@/objects/Gem';

@Component({
  components: {}
})
export default class AddThingy extends Vue {
  private gemsDisplayModule = getModule(GemsDisplayModule);
  private gem: Gem = new Gem();

  async created() {
    this.gem = await this.gemsDisplayModule.getGemById(
      parseInt(this.$route.params.gemId, 10)
    );
    console.log(this.gem);
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';
</style>
