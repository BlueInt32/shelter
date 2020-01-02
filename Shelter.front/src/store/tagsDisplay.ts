import store from './';
import {
  VuexModule,
  Module,
  Action,
  getModule,
  Mutation
} from 'vuex-module-decorators';
import AppService from '../services/app.service';
import { Gem } from '@/objects/Gem';
import { Tag } from '@/objects/Tag';
import { ModalMode } from '@/objects/enums';
import { GemSaveApiModel } from '@/objects/apiModels/GemSaveApiModel';
import { SearchForGemsApiModel } from '@/objects/apiModels/SearchForGemsApiModel';
import { SearchForTagsApiModel } from '@/objects/apiModels/SearchForTagsApiModel';

const appService = new AppService();

@Module({ dynamic: true, namespaced: true, name: 'tagsDisplay', store })
export default class TagsDisplay extends VuexModule {
  @Action({ rawError: true })
  public async searchForTags(searchForTagsApiModel: SearchForTagsApiModel) {
    const tags = await appService.searchForTags(searchForTagsApiModel);
    return tags;
    // // if inputmode is upload, we have to change the model to use base64file
    // const fileinputmodule = getmodule(fileinput);
    // if (fileinputmodule.inputmode === 'upload') {
    //   [postmodel.mimetype, postmodel.base64file] = postmodel.fileurl.split(',');
    //   [postmodel.mimetype] = postmodel.mimetype.split(';');
    //   postmodel.mimetype = postmodel.mimetype.replace('data:', '');
    //   postmodel.fileurl = '';
    // }
    // // console.log('go appservice');
    // return appservice.createpost(postmodel);
  }
}
