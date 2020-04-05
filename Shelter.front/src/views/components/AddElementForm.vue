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
      <fieldset v-if="['video', 'image'].includes($route.params.type)">
        <div class="pure-g">
          <div class="pure-u-3-4">
            <input
              type="text"
              :placeholder="($route.params.type + ' link') | capitalize"
              class="pure-input-1"
              v-model="elementLink"
            />
          </div>
          <div class="pure-u-1-8" :style="{ 'text-align': 'center' }">
            <label> or </label>
          </div>
          <div class="pure-u-1-8">
            <div class="fileUpload pure-button">
              <span>Upload</span>
              <input type="file" class="upload" />
            </div>
          </div>
          <div class="pure-u-1">
            <input
              id="title"
              type="text"
              placeholder="Title"
              v-model="elementTitle"
              class="pure-input-1 pure-u-1"
            />
          </div>
          <div class="pure-u-1">
            <vue-tags-input
              id="form-tags-input"
              class="addTagsInputComponent pure-input-1"
              v-model="tag"
              placeholder="Add some tags"
              :tags="tags"
              :autocomplete-items="autocompleteItems"
              @tags-changed="tagsChangedHandler"
            />
          </div>
        </div>
      </fieldset>

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
  private elementLink: string = '';
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
    elementCreationModel.linkUrl = this.elementLink;
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
#form-tags-input.vue-tags-input {
  margin: 4px 0;
  max-width: 100%;
}
#form-tags-input .ti-input {
  padding: 1px 1px 1px 1px;
}
#form-tags-input .ti-new-tag-input-wrapper {
  padding: 3px 5px;
}

.fileUpload {
  position: relative;
  overflow: hidden;
  width: 100%;
  span {
    cursor: pointer;
  }
}
.fileUpload input.upload {
  position: absolute;
  top: 0;
  right: 0;
  margin: 0;
  padding: 0;
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  filter: alpha(opacity=0);
}
</style>
