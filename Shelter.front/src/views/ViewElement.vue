<template>
  <div class="viewElement">
    <h1>{{ element.title }}</h1>
    <h2>{{ element.text }}</h2>
    <span class="viewElement__info" v-if="element.tags.length === 0"
      >No tag</span
    >
    <ul class="viewElement__tagslist">
      <li v-for="tag in element.tags" :key="tag.id">{{ tag.label }}</li>
    </ul>
    <input type="button" value="Delete" @click="clickDeleteHandler" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import ElementsDisplayModule from '@/store/elementsDisplay';
import ElementEditionModule from '@/store/elementEdition';
import { Element } from '@/objects/Element';
import { notify, NotificationType } from '../services/notificationService';

@Component({
  components: {}
})
export default class ViewElement extends Vue {
  private elementsDisplayModule = getModule(ElementsDisplayModule);
  private elementEditionModule = getModule(ElementEditionModule);
  private element: Element = new Element();
  private $snotify: any;

  async created() {
    this.element = await this.elementsDisplayModule.getElementById(
      parseInt(this.$route.params.elementId, 10)
    );
  }

  async clickDeleteHandler() {
    await this.elementEditionModule.deleteElement(this.element.id);
    notify(this.$snotify, NotificationType.OK, 'Post deleted');
    this.$router.push({ name: 'home' });
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';
.viewElement {
  padding: 2em;
}

.viewElement__info {
  font-style: italic;
  color: #aaa;
}

ul.viewElement__tagslist {
  list-style: none;

  li {
    display: inline;
    border-radius: 3px;
    background: #aaf;
    color: white;
    margin: 0px 2px;
    padding: 2px;
  }
}
</style>
