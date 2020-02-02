<template>
  <div class="">
    <div
      class="email-item email-item-selected pure-g"
      v-for="element in elements"
      :key="element.id"
    >
      <div class="pure-u">
        <img
          width="64"
          height="64"
          alt="Tilo Mitra&#x27;s avatar"
          class="email-avatar"
          src="img/common/tilo-avatar.png"
        />
      </div>
      <div class="pure-u-3-4">
        <h5 class="email-name">{{ element.title }}</h5>
        <h4 class="email-subject">Hello from Toronto</h4>
        <p class="email-desc">
          <router-link
            :to="{ name: 'viewElement', params: { elementId: element.id } }"
            >view</router-link
          >
        </p>
      </div>
    </div>
    <span class="elementsList__info" v-if="!elements || elements.length === 0"
      >No element yet :(</span
    >
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Element } from '@/objects/Element';

@Component
export default class ElementsList extends Vue {
  @Prop() private msg!: string;
  @Prop() private elements!: Element[];

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
  padding: 2em;

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
</style>
