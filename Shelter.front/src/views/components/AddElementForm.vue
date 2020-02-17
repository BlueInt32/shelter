<template>
  <div class="addElement pure-u-1">
    <form class="pure-form pure-form-stacked">
      <!-- TEXT FORM -->
      <fieldset class="pure-group" v-if="$route.params.type === 'text'">
        <input
          type="text"
          class="pure-input-1"
          placeholder="Give a title (optional)"
        />
        <textarea
          class="pure-input-1"
          placeholder="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vitae fermentum velit. Sed convallis at odio eget imperdiet. Donec vulputate diam faucibus lorem molestie, ac mattis quam tincidunt. Nunc tempus metus vel risus vulputate iaculis. Etiam quis nibh nisi. Aenean blandit cursus est. Quisque sagittis, leo nec pretium rutrum, nunc diam vulputate ipsum, id suscipit ipsum libero quis purus. Vivamus mattis, nisl vitae pellentesque accumsan, ex felis pretium nibh, ac luctus magna magna at nisl. Sed euismod orci varius libero vestibulum, eu pellentesque enim tincidunt. "
          rows="10"
        ></textarea>
      </fieldset>

      <!-- IMAGE/VIDEO FORM -->
      <fieldset
        class="pure-group"
        v-if="['video', 'image'].includes($route.params.type)"
      >
        <div class="upload-btn-wrapper pure-input-1">
          <button class="btn button-large">Upload a file</button>
          <input
            type="file"
            name="file"
            ref="file"
            v-on:change="handleFileUpload()"
          />
        </div>
        <!-- <input
          type="file"
          id="file"
          ref="file"
          v-on:change="handleFileUpload()"
        /> -->
      </fieldset>
      <vue-tags-input
        class="addTagsInputComponent pure-input-1"
        v-model="tag"
        :tags="tags"
        :autocomplete-items="autocompleteItems"
        @tags-changed="tagsChangedHandler"
      />

      <fieldset>
        <div class="pure-control-group">
          <label for="title">Title (optional)</label>
          <input
            id="title"
            type="text"
            placeholder=""
            v-model="elementTitle"
            class="pure-input-2-3"
          />
        </div>
        <div class="pure-control-group">
          <label for="text">Link, text, anything...</label>
          <input
            id="text"
            type="text"
            placeholder=""
            v-model="elementText"
            class="pure-input-2-3"
          />
          <span class="pure-form-message-inline">*</span>
        </div>
        <div class="pure-controls">
          <button
            class="pure-button button-success"
            type="button"
            value="Add"
            @click="clickSubmitHandler()"
          >
            Add
          </button>
        </div>
      </fieldset>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import VueTagsInput from '@johmun/vue-tags-input';
import {
  SaveElementApiModel,
  SaveElementWithFileApiModel
} from '@/objects/apiModels/SaveElementApiModel';
import { AutocompleteItem } from '@/objects/AutocompleteItem';
import { getModule } from 'vuex-module-decorators';
import TagsDisplayModule from '@/store/tagsDisplay';
import { SearchForTagsApiModel } from '@/objects/apiModels/SearchForTagsApiModel';

@Component({
  components: {
    VueTagsInput
  }
})
export default class AddElementForm extends Vue {
  private tagsDisplayModule = getModule(TagsDisplayModule);
  private elementText: string = '';
  private elementTitle: string = '';
  private tags: any[] = [];
  private pendingFile: File | null = null;
  private autocompleteItems: AutocompleteItem[] = [];
  private tag: string = '';
  private debounce: any = null;

  @Prop(Function) private submitHandler!: (
    model: SaveElementWithFileApiModel
  ) => void;

  created() {}
  clickSubmitHandler() {
    let elementCreationModel = new SaveElementApiModel();
    elementCreationModel.text = this.elementText;
    elementCreationModel.title = this.elementTitle;
    elementCreationModel.tags = this.tags.map(t => t.text);
    let modelWithFile = new SaveElementWithFileApiModel(
      elementCreationModel,
      this.pendingFile
    );
    this.submitHandler(modelWithFile);
  }

  handleFileUpload() {
    // TODO : find a way to remove the linter error
    // @ts-ignore
    this.pendingFile = this.$refs.file.files[0];
  }
  tagsChangedHandler(newTags: string[]) {
    this.autocompleteItems = [];
    this.tags = newTags;
  }
  async initItems() {
    if (this.tag.length < 2) return;
    clearTimeout(this.debounce);
    this.debounce = setTimeout(async () => {
      let results = await this.tagsDisplayModule.searchForTags(
        new SearchForTagsApiModel(this.tag)
      );
      const mapped = results.map(r => new AutocompleteItem(r.label));
      this.autocompleteItems = mapped;
    }, 300);
  }
  @Watch('tag')
  private tagWatcher() {
    this.initItems();
  }
}
</script>

<style lang="scss">
.upload-btn-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  &:hover {
    .btn {
      border: 2px solid #1f8dd6;
      color: #1f8dd6;
    }
  }
}

.btn {
  font-size: 110%;
  // border: 2px solid gray;
  // color: gray;
  // background-color: white;
  // padding: 8px 20px;
  // border-radius: 8px;
  // font-size: 20px;
  // font-weight: bold;
}

.upload-btn-wrapper input[type='file'] {
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
  font-size: 100px;
  height: 100%;
  width: 100%;
  &:hover {
    cursor: pointer;
  }
}
</style>
