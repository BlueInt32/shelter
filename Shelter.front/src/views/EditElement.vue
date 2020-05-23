<template>
  <div class="editElement pure-u-1">
    <div class="pure-u-1">
      <h1>Edit an element</h1>
      <form class="pure-form pure-form-stacked">
        <fieldset>
          <div class="pure-u-1">
            <input
              id="title"
              type="text"
              placeholder="Title"
              v-model="elementTitle"
              class="pure-input-1 pure-u-1"
            />
          </div>
          <div class="pure-u-3-4">
            <input
              type="text"
              :placeholder="(elementType + ' link') | capitalize"
              class="pure-input-1"
              v-model="elementLinkUrl"
            />
          </div>
          <div class="pure-u-1-8" :style="{ 'text-align': 'center' }">
            <label> or </label>
          </div>
          <div class="pure-u-1-8">
            <div class="fileUpload pure-button">
              <span>Upload</span>
              <input
                type="file"
                class="upload"
                id="file"
                ref="file"
                v-on:change="handleFileUpload"
              />
            </div>
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
  SaveElementBaseApiModel,
  SaveElementWithFileApiModel,
  SaveElementWithLinkApiModel
} from '@/objects/apiModels/SaveElementApiModel';
import { AutocompleteItem } from '@/objects/AutocompleteItem';
import { notify, NotificationType } from '../services/notificationService';
import { Element } from '@/objects/Element';
import VueTagsInput from '@johmun/vue-tags-input';
import { SearchForElementsApiModel } from '../objects/apiModels/SearchForElementsApiModel';
import { SearchForTagsApiModel } from '../objects/apiModels/SearchForTagsApiModel';
import TagInputItem from '@/objects/TagInputItem';
import { ElementType } from '@/objects/apiModels/ElementType';

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
  private elementId: number = 0;

  private elementText: string = '';
  private elementTitle: string = '';
  private elementLinkUrl: string = '';
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
    this.elementLinkUrl = this.element.linkUrl;
    this.elementTitle = this.element.title;
    this.tags = this.element.tags.map(t => new TagInputItem(t.label));
  }
  async updateElement() {
    let elementUpdateModel = new SaveElementBaseApiModel();
    if (this.pendingFile && !this.elementLinkUrl) {
      elementUpdateModel = new SaveElementWithFileApiModel(this.pendingFile);
    } else {
      elementUpdateModel = new SaveElementWithLinkApiModel(this.elementLinkUrl);
    }
    elementUpdateModel.id = this.elementId;
    elementUpdateModel.text = this.elementText;
    elementUpdateModel.title = this.elementTitle;
    elementUpdateModel.tags = this.tags.map(t => t.text);
    elementUpdateModel.type = this.resolveType();

    try {
      if (elementUpdateModel instanceof SaveElementWithFileApiModel) {
        await this.elementEditionModule.updateElementWithFile(
          elementUpdateModel
        );
      } else if (elementUpdateModel instanceof SaveElementWithLinkApiModel) {
        await this.elementEditionModule.updateElementWithLink(
          elementUpdateModel
        );
      }
      notify(this.$snotify, NotificationType.OK, 'Alright !');
      this.$router.push({
        name: 'viewElement',
        params: {
          elementId: this.elementId.toString()
        }
      });
    } catch (e) {
      notify(this.$snotify, NotificationType.ERROR, 'Oops ! ' + e.message);
    }
  }
  resolveType(): ElementType {
    switch (this.elementType) {
      case 'image_link':
        return ElementType.ImageLink;
      case 'image_file':
        return ElementType.ImageFile;
      case 'video_link':
        return ElementType.VideoLink;
      case 'video_file':
        return ElementType.VideoFile;
      case 'web_link':
        return ElementType.WebLink;
    }
    return ElementType.None;
  }

  tagsChangedHandler(newTags: AutocompleteItem[]) {
    this.autocompleteItems = [];
    this.tags = newTags.map(t => new TagInputItem(t.text));
  }

  async initItems() {
    if (this.tag.length < 2) return;
    clearTimeout(this.debounce);
    this.debounce = setTimeout(async () => {
      let results = await this.tagsDisplayModule.searchForTags(
        new SearchForTagsApiModel(this.tag)
      );
      const mapped = results.map(r => {
        return {
          text: r.label
        };
      });
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

  get elementType(): string {
    return this.element.type;
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
