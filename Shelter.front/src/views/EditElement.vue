<template>
  <div class="editElement pure-u-1">
    <div class="pure-u-1">
      <h1>Add an element</h1>
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
              @tags-changed="update"
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
              @click="updateElement()"
            >
              Update
            </button>
          </div>
        </fieldset>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import ElementEditionModule from '@/store/elementEdition';
import ElementsDisplayModule from '@/store/elementsDisplay';
import TagsDisplayModule from '@/store/tagsDisplay';
import {
  SaveElementApiModel,
  SaveElementWithFileApiModel
} from '@/objects/apiModels/SaveElementApiModel';
import { AutocompleteItem } from '@/objects/AutocompleteItem';
import { notify, NotificationType } from '../services/notificationService';
import { Element } from '@/objects/Element';
import VueTagsInput from '@johmun/vue-tags-input';
import { SearchForElementsApiModel } from '../objects/apiModels/SearchForElementsApiModel';
import { SearchForTagsApiModel } from '../objects/apiModels/SearchForTagsApiModel';
import TagInputItem from '@/objects/TagInputItem';

@Component({
  components: {
    VueTagsInput
  }
})
export default class EditElement extends Vue {
  private elementEditionModule = getModule(ElementEditionModule);
  private elementsDisplayModule = getModule(ElementsDisplayModule);
  private tagsDisplayModule = getModule(TagsDisplayModule);
  private element: Element = new Element();
  private elementId: number | null = null;

  private elementText: string = '';
  private elementTitle: string = '';
  private $snotify: any;
  private tag: string = '';
  private tags: TagInputItem[] = [];
  private autocompleteItems: AutocompleteItem[] = [];
  private debounce: any = null;
  private pendingFile: File | null = null;

  async created() {
    this.elementId = parseInt(this.$route.params.elementId, 10);
    this.element = await this.elementsDisplayModule.getElementById(
      this.elementId
    );
    this.elementText = this.element.text;
    this.elementTitle = this.element.title;
    this.tags = this.element.tags.map(t => new TagInputItem(t.label));
  }
  async updateElement() {
    let elementCreationModel = new SaveElementApiModel();

    elementCreationModel.id = this.elementId;
    elementCreationModel.text = this.elementText;
    elementCreationModel.title = this.elementTitle;
    elementCreationModel.tags = this.tags.map(t => t.text);
    const elementUpdateWithFileModel = new SaveElementWithFileApiModel(
      elementCreationModel,
      this.pendingFile
    );
    try {
      await this.elementEditionModule.updateElement(elementUpdateWithFileModel);
      notify(this.$snotify, NotificationType.OK, 'Cool post !');
      this.$router.push(`/view/${this.elementId}`);
    } catch (e) {
      notify(this.$snotify, NotificationType.ERROR, 'Oops ! ' + e.message);
    }
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
  handleFileUpload() {
    // TODO : find a way to remove the linter error
    // @ts-ignore
    this.pendingFile = this.$refs.file.files[0];
  }
  update(newTags: TagInputItem[]) {
    this.autocompleteItems = [];
    this.tags = newTags;
  }
  @Watch('tag')
  private tagWatcher() {
    this.initItems();
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';

.addTagsInputComponent {
  display: inline-block;
}
.ti-input {
  border-radius: 4px;
  box-shadow: inset 0 1px 3px #ddd;
}
input[type='text'].ti-new-tag-input {
  line-height: 22px;
  box-shadow: none;
}
.vue-tags-input .ti-tag {
  position: relative;
  background: $primary;
  color: $tagsAndButtonsColor;
}
</style>
