<template>
  <div class="addThingy">
    <div class="pure-g">
      <div class="pure-u-1-5"></div>
      <div class="pure-u-3-5">
        <h1>Add stuff</h1>
        <form class="pure-form pure-form-aligned">
          <fieldset>
            <legend>
              A "thingy" is something you just want to review later. <br />
              Who knows ? Maybe it would be a gem ?
            </legend>
            <div class="pure-control-group">
              <label for="text">Link, text, anything...</label>
              <input
                id="text"
                type="text"
                placeholder=""
                v-model="gemText"
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
                @tags-changed="newTags => (tags = newTags)"
              />
            </div>
            <div class="pure-control-group">
              <label for="title">Title (optional)</label>
              <input
                id="title"
                type="text"
                placeholder=""
                v-model="gemTitle"
                class="pure-input-2-3"
              />
            </div>
            <div class="pure-controls">
              <button
                class="pure-button pure-button-primary"
                type="button"
                value="Add"
                @click="createGem()"
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
import { Component, Prop, Vue } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import GemEditionModule from '@/store/gemEdition';
import { GemSaveApiModel } from '../objects/apiModels/GemSaveApiModel';
import { notify, NotificationType } from '../services/notificationService';
import VueTagsInput from '@johmun/vue-tags-input';

@Component({
  components: {
    VueTagsInput
  }
})
export default class AddThingy extends Vue {
  private gemEditionModule = getModule(GemEditionModule);

  private gemText: string = '';
  private gemTitle: string = '';
  private $snotify: any;
  private tag: string = '';
  private tags: string[] = [];

  created() {}
  async createGem() {
    let gemCreationModel = new GemSaveApiModel();
    gemCreationModel.text = this.gemText;
    gemCreationModel.title = this.gemTitle;
    try {
      await this.gemEditionModule.createGem(gemCreationModel);
      notify(this.$snotify, NotificationType.OK, 'Cool post !');
    } catch (e) {
      notify(this.$snotify, NotificationType.ERROR, 'Oops ! ' + e.message);
    }
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
  box-shadow: none;
}
.vue-tags-input .ti-tag {
  position: relative;
  background: $main;
  color: #283944;
}
</style>
