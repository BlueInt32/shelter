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
              <input id="text" type="text" placeholder="" v-model="gemText" />
              <span class="pure-form-message-inline">*</span>
            </div>
            <div class="pure-control-group">
              <label for="title">Tags</label>
              <!-- <TagsMiniList
                :tagsList="postEditionModule.stagedTags"
                :keySelector="tag => tag.id"
                :labelSelector="tag => tag.label"
                :tagCrossClickHandler="removeStagedTagHandler"
              />
              <TagsInputComponent
                @commit="tagsCommitHandler"
                :tabindex="2"
              ></TagsInputComponent> -->
              <input id="title" type="text" placeholder="" v-model="gemTitle" />
            </div>
            <div class="pure-control-group">
              <label for="title">Title (optional)</label>
              <input id="title" type="text" placeholder="" v-model="gemTitle" />
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

@Component({
  components: {}
})
export default class AddThingy extends Vue {
  private gemEditionModule = getModule(GemEditionModule);

  private gemText: string = '';
  private gemTitle: string = '';
  private $snotify: any;

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
