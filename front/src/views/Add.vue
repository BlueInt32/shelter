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
              <label for="link">Link, text, anything...</label>
              <input id="link" type="text" placeholder="" v-model="gemLink" />
              <span class="pure-form-message-inline">Mandatory</span>
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

@Component({
  components: {}
})
export default class AddThingy extends Vue {
  private gemEditionModule = getModule(GemEditionModule);

  private gemLink: string = '';
  private gemTitle: string = '';

  created() {}
  createGem() {
    let gemCreationModel = new GemSaveApiModel();
    gemCreationModel.link = this.gemLink;
    gemCreationModel.title = this.gemTitle;
    this.gemEditionModule.createGem(gemCreationModel);
  }
}
</script>
