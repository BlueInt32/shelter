<template>
  <div class="typePrompt pure-u-1 flex-container">
    <div
      @click="clickHandler('image')"
      class="flex-item typePrompt__buttonwrapper"
    >
      <div class="flex-item-content">
        <font-awesome-icon class="typePrompt__icon" icon="image" /> Image
      </div>
    </div>
    <div
      @click="clickHandler('video')"
      class="flex-item typePrompt__buttonwrapper"
    >
      <div class="flex-item-content">
        <font-awesome-icon class="typePrompt__icon" icon="video" /> Video
      </div>
    </div>
    <div
      @click="clickHandler('text')"
      class="flex-item typePrompt__buttonwrapper"
    >
      <div class="flex-item-content">
        <font-awesome-icon class="typePrompt__icon" icon="align-left" /> Text
      </div>
    </div>
    <div
      @click="clickHandler('link')"
      class="flex-item typePrompt__buttonwrapper"
    >
      <div class="flex-item-content">
        <font-awesome-icon class="typePrompt__icon" icon="link" /> Link
      </div>
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
.flex-container {
  padding: 0;
  margin: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
}
.flex-item {
  box-sizing: border-box;
  background: $primary;
  margin: 5px;
  color: white;
  font-weight: bold;
  font-size: 2rem;
  text-align: center;
  flex: 0 0 50%;
  height: auto;
  display: flex;
  border: 3px solid white;
  padding: 10px;
  text-align: center;
  margin: 0 auto;
  position: relative;
  cursor: pointer;
  max-height: 40vh;

  &:hover {
    background: $primaryHover;
  }
}
.flex-item-content {
  position: absolute;
  display: block;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  width: 50%;
  height: 10%;
  margin: auto;
}
.flex-item:before {
  content: '';
  display: inline-block;
  vertical-align: middle;
  padding-top: 100%;
}
</style>
