<template>
  <div class="gemsList">
    <p v-for="gemCategory in gemsCategories" :key="gemCategory.id">
      {{ gemCategory.id }} - {{ gemCategory.title }}
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { GemCategoryViewModel } from '../viewModels/GemCategoryViewModel';

@Component
export default class GemsList extends Vue {
  @Prop() private msg!: string;
  @Prop() private gemsCategories!: GemCategoryViewModel[];

  created() {
    console.log(this.gemsCategories);
  }
}
</script>
