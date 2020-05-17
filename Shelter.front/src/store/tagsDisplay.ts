import store from './';
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
import { SearchForElementsApiModel } from '@/objects/apiModels/SearchForElementsApiModel';
import { SearchForTagsApiModel } from '@/objects/apiModels/SearchForTagsApiModel';

const appService = new AppService();

@Module({ dynamic: true, namespaced: true, name: 'tagsDisplay', store })
export default class TagsDisplay extends VuexModule {
  @Action({ rawError: true })
  public async searchForTags(searchForTagsApiModel: SearchForTagsApiModel) {
    return appService.searchForTags(searchForTagsApiModel);
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
}
