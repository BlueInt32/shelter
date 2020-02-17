<template>
  <div class="addElement pure-u-1">
    <form class="pure-form pure-form-aligned">
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
        <div class="pure-control-group">
          <label for="title">Tags</label>
          <vue-tags-input
            class="addTagsInputComponent pure-input-2-3"
            v-model="tag"
            :tags="tags"
            :autocomplete-items="autocompleteItems"
            @tags-changed="tagsChangedHandler"
          />
        </div>
        <div class="pure-controls">
          <input
            type="file"
            id="file"
            ref="file"
            v-on:change="handleFileUpload()"
          />
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
