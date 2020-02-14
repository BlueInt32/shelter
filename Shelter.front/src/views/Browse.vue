<template>
  <div>
    <div id="list" class="home pure-u-1">
      <ElementsList :elements="elements" />
    </div>
    <div class="pure-u"></div>
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
  async created() {
    this.elements = await this.elementsDisplayModule.searchForElements(
      new SearchForElementsApiModel()
    );
  }
}
</script>
