<template>
  <div class="tagsInput">
    <div class="tagsInputContainer autocomplete-input">
      <input
        id="tagsearchinput"
        class="form-control"
        placeholder="Search for tags"
        type="text"
        v-bind:value="searchText"
        v-on:input="changeHandler"
        v-on:keydown.down="down()"
        v-on:keydown.up="up()"
        v-on:keydown.esc="escapeKeyHandler()"
        v-on:keydown.enter="enterKeyHandler()"
        v-on:blur="escapeKeyHandler()"
        v-on:focus="focusHandler()"
        :tabindex="tabindex"
      />
      <ul v-show="isListVisibleLocal" class="options-list">
        <li
          v-for="(result, index) in tagsSearchResults"
          v-bind:key="result.id"
          v-on:mouseover="hoverResultHandler(index)"
          v-on:mouseout="setOverResults(false)"
          v-on:click="clickKnownTagHandler"
          v-bind:class="{ selected: currentlySelectedIndex === index }"
        >
          {{ result.label }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import TagsInput from '@/modules/tagsInput';
import PostEdition from '@/modules/postEdition';
import { Tag } from '@/types/interfaces';

@Component({
  components: {}
})
export default class TagsInputComponent extends Vue {
  private overResults: boolean = false;
  @Prop(Number) private tabindex: number;
  private tagsInputModule = getModule(TagsInput);
  private postEditionModule = getModule(PostEdition);

  private get tagsSearchResults() {
    return this.tagsInputModule.tagsSearchResults;
  }
  private get searchText() {
    return this.tagsInputModule.searchText;
  }
  private get isListVisibleLocal() {
    return this.tagsInputModule.isListVisible;
  }
  private get currentlySelectedIndex() {
    return this.tagsInputModule.currentlySelectedIndex;
  }

  private changeHandler(event) {
    this.tagsInputModule.updateText({
      text: event.target.value,
      excludedTagsIds: this.postEditionModule.stagedTags.map(t => t.id),
      showAllIfEmptySearch: false
    });
  }
  private focusHandler() {
    this.tagsInputModule.check();
  }
  private escapeKeyHandler() {
    if (!this.overResults) {
      this.tagsInputModule.escape();
    }
  }
  private setOverResults(val) {
    this.overResults = val;
  }
  private down() {
    this.tagsInputModule.selectDown();
  }
  private up() {
    this.tagsInputModule.selectUp();
  }
  private hoverResultHandler(index) {
    this.tagsInputModule.setSelection(index);
    this.setOverResults(true);
  }
  private enterKeyHandler() {
    this.tagsInputModule.commitTag().then(tagsToEmit => {
      tagsToEmit.forEach(tag => {
        this.$emit('commit', tag);
      });
      this.tagsInputModule.resetEmittedTags();
    });
  }
  private clickKnownTagHandler() {
    this.tagsInputModule.commitKnownTag();
    this.$emit('commit', this.tagsInputModule.tagsInputCommittedSelection);
  }
  private mounted() {
    this.tagsInputModule.escape();
  }
}
</script>

<style scoped lang="scss">
@import '../css/custom.scss';
.tagsInput {
  max-height: 32px;
}

ul {
  list-style-type: none;
  padding: 0;
  z-index: 10;
}
li {
  display: inline-block;
  margin: 0 10px;
}
input {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}
.autocomplete-input {
  position: relative;
}
ul.options-list {
  display: flex;
  flex-direction: column;
  margin: 0px;
  border: 1px solid #dbdbdb;
  border-radius: 0 0 3px 3px;
  position: absolute;
  width: 100%;
  overflow: hidden;
}
ul.options-list li {
  width: 100%;
  flex-wrap: wrap;
  background: white;
  margin: 0;
  border-bottom: 1px solid #eee;
  color: #363636;
  padding: 7px;
  cursor: pointer;

  &.selected {
    background: #fdd5ff;
  }
}
ul.options-list li.highlighted {
  background: #f8f8f8;
}
.tag {
  margin-right: 3px;
}
</style>
