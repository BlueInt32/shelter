<template>
  <div class="elementsList__container">
    <span class="elementsList__loading" v-if="loading">
      <!--  -->
      <font-awesome-icon
        class="elementsList__loader"
        icon="circle-notch"
        spin
      />
      Loading elements...
    </span>
    <span
      class="elementsList__info"
      v-if="!loading && (!elements || elements.length === 0)"
      >No element yet :(</span
    >
    <div
      class="elementsList__item"
      v-for="element in elements"
      :key="element.id"
    >
      <router-link
        class="elementsList__innerBox"
        :to="{ name: 'viewElement', params: { elementId: element.id } }"
      >
        <h4 v-if="element.title" :title="element.title">{{ element.title }}</h4>
        <img v-if="element.type !== 'web_link'" :src="element.thumbnailUrl" />
        <span class="elementsList__linkSpan" v-else>{{ element.linkUrl }}</span>
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Element } from '@/objects/Element';

@Component({})
export default class ElementsList extends Vue {
  @Prop() private elements!: Element[];
  @Prop(Boolean) private loading!: boolean;

  created() {}
}
</script>

<style lang="scss">
.elementsList__info {
  font-style: italic;
  color: #aaa;
}
.elementsList__container {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: stretch;
  align-content: stretch;
  padding: 1em;

  .elementsList__item {
    // height: 70px;
    overflow: hidden;
    width: 13vw;
    height: 15vh;
    padding: 4px;

    p {
      margin: 0.1em;
    }
    h4 {
      margin: 0.3em 0;
      font-size: 1em;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .elementsList__innerBox {
      display: block;
      color: inherit;
      text-decoration: none;
      padding: 0.3em;
      height: calc(100% - 8px);
      text-align: center;
      background-color: white;

      img {
        max-height: 100%;
        max-width: 100%;
      }

      .elementsList__tagsList {
        font-size: 0.8em;
      }
    }
  }
}
.elementsList__loading {
  display: inline-block;
  height: 40vh;
  width: 100%;
  line-height: 2em;
  line-height: 40vh;
  margin: 0 auto;
  text-align: center;
}
.elementsList__loader {
  position: relative;
  top: 5px;
  left: 5px;
  margin-right: 10px;
  font-size: 2em;
}
.elementsList__linkSpan {
  display: inline-block;
  max-width: calc(100%);
  text-overflow: clip;
  overflow: hidden;
  overflow-wrap: normal;
}
</style>
