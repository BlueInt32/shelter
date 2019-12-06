<template>
  <div class="addThingy">
    <p>
      A "thingy" is something you just want to review later. <br />
      Who knows ? Maybe it would be a gem ?
    </p>
    <p>Name (optional) <input type="text" /></p>
    <p>Info, link, anything ...? <input type="" /></p>
    <p><input type="button" value="Add" /></p>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({
  components: {}
})
export default class AddThingy extends Vue {
  created() {}
}
</script>
