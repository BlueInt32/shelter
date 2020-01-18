<template>
  <div class="gemsList__container">
    <div class="gemsList__item" v-for="gem in gems" :key="gem.id">
      <div class="gemsList__innerBox">
        <h2>{{ gem.title }}</h2>
        <p class="gemsList__tagsList">
          {{ gem.tags.map(t => t.label).join(', ') }}
        </p>
        <router-link :to="{ name: 'viewGem', params: { gemId: gem.id } }"
          >view</router-link
        >
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Gem } from '@/objects/Gem';

@Component
export default class GemsList extends Vue {
  @Prop() private msg!: string;
  @Prop() private gems!: Gem[];

  created() {}
}
</script>

<style lang="scss" scoped>
.gemsList__container {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: stretch;
  align-content: stretch;

  .gemsList__item {
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

    .gemsList__innerBox {
      padding: 0.3em;
      border: 1px solid gray;

      .gemsList__tagsList {
        font-size: 0.8em;
      }
    }
  }
}
</style>
