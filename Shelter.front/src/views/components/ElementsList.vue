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
      <div class="elementsList__innerBox">
        <h2>{{ element.title }}</h2>
        <router-link
          :to="{ name: 'viewElement', params: { elementId: element.id } }"
          >view</router-link
        >
      </div>
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
    min-width: 10vw;
    max-width: 40vw;
    min-height: 10vh;
    min-height: 15vh;
    padding: 0.3em;

    p {
      margin: 0.1em;
    }
    h2 {
      margin: 0.3em 0;
      font-size: 1.3em;
    }

    .elementsList__innerBox {
      padding: 0.3em;
      border: 1px solid gray;

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
</style>
