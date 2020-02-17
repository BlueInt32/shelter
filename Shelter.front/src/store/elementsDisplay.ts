import store from '.';
import {
  VuexModule,
  Module,
  Action,
  getModule,
  Mutation
} from 'vuex-module-decorators';
import AppService from '../services/app.service';
import { Element } from '@/objects/Element';
import { Tag } from '@/objects/Tag';
import { ModalMode } from '@/objects/enums';
import { SaveElementApiModel } from '@/objects/apiModels/SaveElementApiModel';
import { SearchForElementsApiModel } from '@/objects/apiModels/SearchForElementsApiModel';

const appService = new AppService();

@Module({ dynamic: true, namespaced: true, name: 'elementsDisplay', store })
export default class ElementsDisplay extends VuexModule {
  // modalMode : are we adding or editing a post ?
  public modalMode: ModalMode = ModalMode.Add;
  // isEditing is true whenever we have the postEditionModal open (in both Add and Edit modes)
  public isEditing: boolean = false;
  public stagedTags: Tag[] = [];
  public isPristine: boolean = true;
  private implications = {
    drum: ['music']
  };

  @Action({ rawError: true })
  public async searchForElements(
    searchForElementsApiModel: SearchForElementsApiModel
  ) {
    const elements = await appService.searchForElements(
      searchForElementsApiModel
    );
    return elements;
    // // if inputmode is upload, we have to change the model to use base64file
    // const fileinputmodule = getmodule(fileinput);
    // if (fileinputmodule.inputmode === 'upload') {
    //   [postmodel.mimetype, postmodel.base64file] = postmodel.fileurl.split(',');
    //   [postmodel.mimetype] = postmodel.mimetype.split(';');
    //   postmodel.mimetype = postmodel.mimetype.replace('data:', '');
    //   postmodel.fileurl = '';
    // }
    // return appservice.createpost(postmodel);
  }
  @Action({ rawError: true })
  public async getElementById(elementId: number) {
    const element = await appService.getElementById(elementId);
    element.fileUrl = appService.getElementFileUrlById(elementId);
    return element;
  }
}
