<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    <GemsList :gemsCategories="gemsCategories" />
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue';
import GemsList from '@/components/GemsList.vue';

@Component({
  components: {
    HelloWorld,
    GemsList
  }
})
export default class Home extends Vue {
  private gemsCategories = null;
  created() {
    console.log(this.gemsCategories);
    this.gemsCategories = this.$store.state.gemsCategories;
  }
}
</script>
