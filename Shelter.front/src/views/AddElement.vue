<template>
  <div class="addElement pure-u-1">
    <h1 v-if="$route.name == 'addElementStep1'">
      Add an element - Choose the type
    </h1>
    <h1 v-if="$route.name == 'addElementStep2'">
      Add an element - {{ $route.params.type | capitalize }}
    </h1>
    <AddElementTypePrompt
      v-if="$route.name == 'addElementStep1'"
      :choiceHandler="choiceHandler2"
    ></AddElementTypePrompt>
    <AddElementForm
      v-if="$route.name == 'addElementStep2'"
      :submitHandler="createElement"
    >
    </AddElementForm>
  </div>
</template>

<script lang="ts">
// @ is an alias to /src
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import { getModule } from 'vuex-module-decorators';
import ElementEditionModule from '@/store/elementEdition';
import TagsDisplayModule from '@/store/tagsDisplay';
import {
  SaveElementApiModel,
  SaveElementWithFileApiModel
} from '@/objects/apiModels/SaveElementApiModel';
import { AutocompleteItem } from '@/objects/AutocompleteItem';
import { notify, NotificationType } from '../services/notificationService';
import VueTagsInput from '@johmun/vue-tags-input';
import { SearchForElementsApiModel } from '../objects/apiModels/SearchForElementsApiModel';
import { SearchForTagsApiModel } from '../objects/apiModels/SearchForTagsApiModel';
import { RawLocation } from 'vue-router';
import { CreationStep } from '@/objects/enums/CreationStep';
import AddElementTypePrompt from '@/views/components/AddElementTypePrompt.vue';
import AddElementForm from '@/views/components/AddElementForm.vue';

@Component({
  components: {
    VueTagsInput,
    AddElementTypePrompt,
    AddElementForm
  }
})
export default class AddElement extends Vue {
  private elementEditionModule = getModule(ElementEditionModule);

  private $snotify: any;
  private creationStep: CreationStep = CreationStep.PromptType;
  private creationStepEnum = CreationStep;

  created() {}

  async createElement(model: SaveElementWithFileApiModel) {
    try {
      let data = await this.elementEditionModule.createElement(model);
      notify(this.$snotify, NotificationType.OK, 'Cool post !');
      this.$router.push({
        name: 'viewElement',
        params: { elementId: data.id.toString() }
      });
    } catch (e) {
      notify(this.$snotify, NotificationType.ERROR, 'Oops ! ' + e.message);
    }
  }

  choiceHandler2(choice: string) {
    // this.creationStep = CreationStep.Form;
    this.$router.push({ name: 'addElementStep2', params: { type: choice } });
  }
}
</script>

<style lang="scss">
@import '@/styles/custom.scss';

.addTagsInputComponent {
  display: inline-block;
  max-width: 100%;
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
