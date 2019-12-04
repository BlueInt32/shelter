<template>
  <div class="gemsList">
    <p v-for="gemCategory in gemCategories" :key="gemCategory.id">
      {{ gemCategory.title }}
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { GemCategoryViewModel } from '../viewModels/GemCategoryViewModel';

@Component
export default class GemsList extends Vue {
  @Prop() private msg!: string;
  @Prop() private gemCategories!: GemCategoryViewModel[];
}
</script>
