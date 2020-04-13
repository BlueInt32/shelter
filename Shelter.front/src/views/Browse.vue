<template>
  <div id="list" class="home pure-u-1">
    <h1>Browse elements</h1>
    <ElementsList :loading="loading" :elements="elements" />
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
export default class Browse extends Vue {
  private elements: any = null;
  private elementsDisplayModule: ElementsDisplayModule = getModule(
    ElementsDisplayModule
  );
  private loading: boolean = true;

  async created() {
    this.elements = await this.elementsDisplayModule.searchForElements(
      new SearchForElementsApiModel()
    );
    console.log(this.elements);
    this.loading = false;
  }
}
</script>
