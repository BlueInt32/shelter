<template>
  <div class="viewElement pure-u">
    <h1>{{ element.title }}</h1>
    <p v-if="element.text">{{ element.text }}</p>
    <span class="viewElement__date">
      {{ dateFormatted }}
    </span>
    <button class="pure-button" @click="clickEditHandler">
      Edit
    </button>
    <button class="pure-button button-error" @click="clickDeleteHandler">
      Delete
    </button>
    <span class="viewElement__info" v-if="element.tags.length === 0"
      >No tag</span
    >
    <ul class="viewElement__tagslist">
      <li v-for="tag in element.tags" :key="tag.id">{{ tag.label }}</li>
    </ul>
    <div class="fileContainer">
      <img
        :src="element.fileUrl"
        v-if="baseElementType === 'image'"
        class="viewElement__mainMedia"
      />
      <video
        class="viewElement__mainMedia"
        width="800"
        controls
        autoplay
        :src="element.fileUrl"
        v-if="baseElementType === 'video'"
      />
      <a
        target="_blank"
        class="viewElement__mainWebLink"
        :href="element.linkUrl"
        v-if="baseElementType === 'web_link'"
        >{{ element.linkUrl }}</a
      >
    </div>
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
import { ElementType } from '@/objects/apiModels/ElementType';

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
    this.dateFormatted = dayjs(this.element.creation_date).format(
      'DD/MM/YYYY HH:mm:ss'
    );
  }

  async clickDeleteHandler() {
    await this.elementEditionModule.deleteElement(this.element.id);
    notify(this.$snotify, NotificationType.OK, 'Post deleted');
    this.$router.push({ name: 'browse' });
  }
  async clickEditHandler() {
    this.$router.push(`/edit/${this.element.id}`);
  }

  get baseElementType(): string {
    switch (this.element.type) {
      case ElementType.ImageLink:
        return 'image';
      case ElementType.ImageFile:
        return 'image';
      case ElementType.VideoLink:
        return 'video';
      case ElementType.VideoFile:
        return 'video';
      case ElementType.WebLink:
        return 'web_link';
    }
    return '';
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';

.viewElement__info {
  font-style: italic;
  color: #aaa;
}
.viewElement__date {
  font-size: 0.8em;
  font-style: italic;
  color: #aaa;
}

ul.viewElement__tagslist {
  margin: 9px 0;
  padding: 0;
  list-style: none;

  li {
    display: inline;
    border-radius: 2px;
    background: $primary;
    color: white;
    margin: 0 2px 0 0;
    padding: 4px;
  }
}
.fileContainer {
  img {
    max-width: calc(100vw - 2em);
  }
}
.viewElement__mainMedia {
  max-height: 75vh;
}
.viewElement__mainWebLink {
  color: $linkColor;
  font-size: 1.3em;
}
</style>
