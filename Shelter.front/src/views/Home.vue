<template>
  <div class="pure-u">
    <h1>Home page</h1>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ElementsList from '@/views/components/ElementsList.vue';
import { getModule } from 'vuex-module-decorators';
import ElementsDisplayModule from '@/store/elementsDisplay';
import { SearchForElementsApiModel } from '../objects/apiModels/SearchForElementsApiModel';

@Component({
  components: {
    ElementsList
  }
})
export default class Home extends Vue {
  private elements: any = null;
  private elementsDisplayModule: ElementsDisplayModule = getModule(
    ElementsDisplayModule
  );
  private loading: boolean = true;

  async created() {
    this.elements = await this.elementsDisplayModule.searchForElements(
      new SearchForElementsApiModel()
    );
    this.loading = false;
  }
}
</script>
