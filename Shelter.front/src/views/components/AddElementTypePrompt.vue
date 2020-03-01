<template>
  <div class="typePrompt pure-u-1">
    <div class="typePrompt__buttonwrapper">
      <a @click="clickHandler('image')">
        <font-awesome-icon class="typePrompt__icon" icon="image" />Image
      </a>
    </div>
    <div class="typePrompt__buttonwrapper">
      <a @click="clickHandler('video')">
        <font-awesome-icon class="typePrompt__icon" icon="video" />Video
      </a>
    </div>
    <div class="typePrompt__buttonwrapper">
      <a @click="clickHandler('text')">
        <font-awesome-icon class="typePrompt__icon" icon="align-left" />Text
      </a>
    </div>
    <div class="typePrompt__buttonwrapper">
      <a @click="clickHandler('link')">
        <font-awesome-icon class="typePrompt__icon" icon="link" />Link
      </a>
    </div>
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
<style lang="scss">
@import '@/styles/custom.scss';

.typePrompt__buttonwrapper {
  position: relative;
  width: 49%;
  padding-bottom: 50%;
  margin: 3px;
  background: none;
}
.typePrompt a {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  font-size: 2em;
  border-radius: 10px;
  border: 3px solid $primary;
  background: none;
  :hover {
    background-color: $primary;
    color: white;
  }
}
.typePrompt__icon {
  position: relative;
  top: 13px;
  left: 0px;
  margin-right: 22px;
  font-size: 2em;
}
</style>
