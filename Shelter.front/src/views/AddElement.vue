<template>
  <div class="addElement">
    <div class="pure-g">
      <div class="pure-u-1-5"></div>
      <div class="pure-u-3-5">
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
              <button
                class="pure-button button-success"
                type="button"
                value="Add"
                @click="createElement()"
              >
                Add
              </button>
            </div>
          </fieldset>
        </form>
      </div>
      <div class="pure-u-1-5"></div>
    </div>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import ElementEditionModule from '@/store/elementEdition';
import TagsDisplayModule from '@/store/tagsDisplay';
import { SaveElementApiModel } from '@/objects/apiModels/SaveElementApiModel';
import { AutocompleteItem } from '@/objects/AutocompleteItem';
import { notify, NotificationType } from '../services/notificationService';
import VueTagsInput from '@johmun/vue-tags-input';
import { SearchForElementsApiModel } from '../objects/apiModels/SearchForElementsApiModel';
import { SearchForTagsApiModel } from '../objects/apiModels/SearchForTagsApiModel';

@Component({
  components: {
    VueTagsInput
  }
})
export default class AddElement extends Vue {
  private elementEditionModule = getModule(ElementEditionModule);
  private tagsDisplayModule = getModule(TagsDisplayModule);

  private elementText: string = '';
  private elementTitle: string = '';
  private $snotify: any;
  private tag: string = '';
  private tags: any[] = [];
  private autocompleteItems: AutocompleteItem[] = [];
  private debounce: any = null;

  created() {}
  async createElement() {
    let elementCreationModel = new SaveElementApiModel();
    elementCreationModel.text = this.elementText;
    elementCreationModel.title = this.elementTitle;
    elementCreationModel.tags = this.tags.map(t => t.text);
    try {
      await this.elementEditionModule.createElement(elementCreationModel);
      notify(this.$snotify, NotificationType.OK, 'Cool post !');
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
  update(newTags: string[]) {
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
