<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png" /> -->
    <GemsList :gems="gems" />
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue } from 'vue-property-decorator';
import GemsList from '@/views/components/GemsList.vue';
import { getModule } from 'vuex-module-decorators';
import GemsDisplayModule from '@/store/gemsDisplay';
import { SearchForGemsApiModel } from '../objects/apiModels/SearchForGemsApiModel';

@Component({
  components: {
    GemsList
  }
})
export default class Home extends Vue {
  private gems: any = null;
  private gemsDisplayModule: GemsDisplayModule = getModule(GemsDisplayModule);
  async created() {
    console.log('created');
    this.gems = await this.gemsDisplayModule.searchForGems(
      new SearchForGemsApiModel()
    );
    console.log('result', this.gems);
  }
}
</script>
