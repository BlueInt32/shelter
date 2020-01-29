<template>
  <div class="viewElement">
    <h1>{{ element.title }}</h1>
    <h2>{{ element.text }}</h2>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import ElementsDisplayModule from '@/store/elementsDisplay';
import { Element } from '@/objects/Element';

@Component({
  components: {}
})
export default class ViewElement extends Vue {
  private elementsDisplayModule = getModule(ElementsDisplayModule);
  private element: Element = new Element();

  async created() {
    this.element = await this.elementsDisplayModule.getElementById(
      parseInt(this.$route.params.elementId, 10)
    );
    console.log(this.element);
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';
</style>
