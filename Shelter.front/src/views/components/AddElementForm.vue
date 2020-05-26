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
      <fieldset v-if="['link'].includes($route.params.type)">
        <div class="pure-g">
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
            <input
              type="text"
              :placeholder="$route.params.type | capitalize"
              class="pure-input-1"
              v-model="elementLink"
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
          :disabled="isDisabled"
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
  SaveElementBaseApiModel,
  SaveElementWithFileApiModel,
  SaveElementWithLinkApiModel
} from '@/objects/apiModels/SaveElementApiModel';
import { AutocompleteItem } from '@/objects/AutocompleteItem';
import { getModule } from 'vuex-module-decorators';
import TagsDisplayModule from '@/store/tagsDisplay';
import { SearchForTagsApiModel } from '@/objects/apiModels/SearchForTagsApiModel';
import { ElementType } from '@/objects/apiModels/ElementType';

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
    model: SaveElementBaseApiModel
  ) => void;
  @Prop(Boolean) private isDisabled!: boolean;

  created() {}

  clickSubmitHandler() {
    const elementType = this.resolveElementType();
    let elementCreationModel = null;
    switch (elementType) {
      case ElementType.ImageLink:
        {
          elementCreationModel = new SaveElementWithLinkApiModel(
            this.elementLink
          );
        }
        break;
      case ElementType.ImageFile:
        {
          elementCreationModel = new SaveElementWithFileApiModel(
            this.pendingFile
          );
        }
        break;
      case ElementType.VideoLink:
        {
          elementCreationModel = new SaveElementWithLinkApiModel(
            this.elementLink
          );
        }
        break;
      case ElementType.VideoFile:
        {
          elementCreationModel = new SaveElementWithFileApiModel(
            this.pendingFile
          );
        }
        break;
      case ElementType.WebLink:
        {
          elementCreationModel = new SaveElementWithLinkApiModel(
            this.elementLink
          );
        }
        break;
    }
    if (!elementCreationModel) {
      throw Error('Element type could not be resolved');
    }

    elementCreationModel.type = elementType;
    elementCreationModel.text = this.elementText;
    elementCreationModel.title = this.elementTitle;
    elementCreationModel.tags = this.tags.map(t => t.text);
    this.submitHandler(elementCreationModel);
  }

  resolveElementType(): ElementType {
    switch (this.$route.params.type) {
      case 'video': {
        if (this.pendingFile && !this.elementLink) {
          return ElementType.VideoFile;
        } else {
          return ElementType.VideoLink;
        }
      }
      case 'image': {
        if (this.pendingFile && !this.elementLink) {
          return ElementType.ImageFile;
        } else {
          return ElementType.ImageLink;
        }
      }
      case 'link': {
        return ElementType.WebLink;
      }
    }
    return ElementType.None;
  }

  handleFileUpload() {
    this.pendingFile = this.uploadedFileContainer.files[0];
  }

  get uploadedFileContainer(): any {
    return this.$refs.file as any;
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
      const mapped = results.map(r => {
        return {
          text: r.label
        };
      });
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
