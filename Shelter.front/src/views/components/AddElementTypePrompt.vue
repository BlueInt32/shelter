<template>
  <div class="typePrompt pure-u">
    <h4>Type prompt</h4>
    <button @click="clickHandler('text')">Text</button>
    <button @click="clickHandler('image')">Image</button>
    <button @click="clickHandler('video')">Video</button>
    <button @click="clickHandler('link')">Link</button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';

@Component({})
export default class AddElementTypePrompt extends Vue {
  @Prop(Function) public readonly choiceHandler!: (choice: string) => void;

  clickHandler(choice: string) {
    this.choiceHandler(choice);
  }
}
</script>
