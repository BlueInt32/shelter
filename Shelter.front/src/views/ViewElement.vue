<template>
  <div class="viewElement pure-u">
    <h1>{{ element.title }}</h1>
    <p>{{ element.text }}</p>
    <span>
      {{ dateFormatted }}
    </span>
    <span class="viewElement__info" v-if="element.tags.length === 0"
      >No tag</span
    >
    <ul class="viewElement__tagslist">
      <li v-for="tag in element.tags" :key="tag.id">{{ tag.label }}</li>
    </ul>
    <div class="fileContainer">
      <img :src="element.fileUrl" />
    </div>
    <button class="pure-button" @click="clickEditHandler">
      Edit
    </button>
    <button class="pure-button button-error" @click="clickDeleteHandler">
      Delete
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import ElementsDisplayModule from '@/store/elementsDisplay';
import ElementEditionModule from '@/store/elementEdition';
import { Element } from '@/objects/Element';
import { notify, NotificationType } from '../services/notificationService';
import dayjs from 'dayjs';

@Component({
  components: {}
})
export default class ViewElement extends Vue {
  private elementsDisplayModule = getModule(ElementsDisplayModule);
  private elementEditionModule = getModule(ElementEditionModule);
  private element: Element = new Element();
  private $snotify: any;
  private dateFormatted: string = '';

  async created() {
    const elementId = parseInt(this.$route.params.elementId, 10);
    this.element = await this.elementsDisplayModule.getElementById(elementId);
    const today = dayjs();
    const formatted = dayjs(this.element.creation_date).format(
      'le DD/MM/YYYY à HH:mm:ss'
    );
    this.dateFormatted = this.element.creation_date;
    this.dateFormatted = `Created ${today
      .diff(dayjs(this.element.creation_date))
      .toString()}ms ago (${formatted})`;
  }

  async clickDeleteHandler() {
    await this.elementEditionModule.deleteElement(this.element.id);
    notify(this.$snotify, NotificationType.OK, 'Post deleted');
    this.$router.push({ name: 'home' });
  }
  async clickEditHandler() {
    this.$router.push(`/edit/${this.element.id}`);
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';

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
.fileContainer {
  img {
    max-width: 50vw;
  }
}
</style>
