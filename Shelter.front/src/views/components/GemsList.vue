<template>
  <div class="gemsList">
    <p v-for="gem in gems" :key="gem.id">{{ gem.id }} - {{ gem.title }}</p>
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
