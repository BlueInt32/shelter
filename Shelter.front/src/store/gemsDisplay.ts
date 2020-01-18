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

const appService = new AppService();

@Module({ dynamic: true, namespaced: true, name: 'gemsDisplay', store })
export default class GemsDisplay extends VuexModule {
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
  public async searchForGems(searchForGemsApiModel: SearchForGemsApiModel) {
    const gems = await appService.searchForGems(searchForGemsApiModel);
    return gems;
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
  @Action({ rawError: true })
  public async getGemById(gemId: number) {
    const gem = await appService.getGemById(gemId);
    return gem;
  }
}
