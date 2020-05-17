import store from '.';
import {
  VuexModule,
  Module,
  Action,
  getModule,
  Mutation
} from 'vuex-module-decorators';
import AppService from '../services/app.service';
// import Posts from './posts';
// import FileInput from './fileInput';
import { Element } from '@/objects/Element';
import { Tag } from '@/objects/Tag';
import { ModalMode } from '@/objects/enums';
import {
  SaveElementBaseApiModel,
  SaveElementWithFileApiModel,
  SaveElementWithLinkApiModel
} from '@/objects/apiModels/SaveElementApiModel';

const appService = new AppService();

const implicationsOrEmpty = (inputLabel: string, implications: any) => {
  if (implications[inputLabel]) {
    return implications[inputLabel].map((label: string) => {
      return { label };
    });
  } else {
    return [];
  }
};
const tagsUnion = (left: Tag[], right: Tag[]) => {
  let outArray = [...left];
  right.forEach(tag => {
    if (!outArray.find(t => t.label === tag.label)) {
      outArray.push(tag);
    }
  });
  return outArray;
};
@Module({ dynamic: true, namespaced: true, name: 'elementEdition', store })
export default class ElementEdition extends VuexModule {
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
  public createElementWithFile(
    data: SaveElementWithFileApiModel
  ): Promise<Element> {
    return appService.createElementWithFile(data);
    // // if inputMode is upload, we have to change the model to use base64File
    // const fileInputModule = getModule(FileInput);
    // if (fileInputModule.inputMode === 'upload') {
    //   [postModel.mimeType, postModel.base64File] = postModel.fileUrl.split(',');
    //   [postModel.mimeType] = postModel.mimeType.split(';');
    //   postModel.mimeType = postModel.mimeType.replace('data:', '');
    //   postModel.fileUrl = '';
    // }
    // return appService.createPost(postModel);
  }

  @Action({ rawError: true })
  public createElementWithLink(
    data: SaveElementWithLinkApiModel
  ): Promise<Element> {
    return appService.createElementWithLink(data);
  }

  @Action({ rawError: true })
  public updateElement(saveElementApiModel: SaveElementWithFileApiModel) {
    return appService.updateElementWithPut(saveElementApiModel);
  }

  @Action({ rawError: true })
  public deleteElement(elementId: number) {
    return new Promise(resolve => {
      appService.deleteElement(elementId).then(data => {
        resolve(data);
      });
    });
  }

  @Mutation
  public startAddingPost() {
    this.isEditing = true;
    this.modalMode = ModalMode.Add;
    this.isPristine = true;
  }

  @Mutation
  public setStagedTags(tags: Tag[]) {
    this.stagedTags = tags;
  }

  @Mutation
  public addStagedTagAndImplications(tag: Tag) {
    const implications = implicationsOrEmpty(tag.label, this.implications);
    this.stagedTags = tagsUnion(this.stagedTags, [tag, ...implications]);
  }
  @Mutation
  public removeStagedTag(tag: Tag) {
    const tagIndex = this.stagedTags.findIndex(t => t.label === tag.label);
    if (tagIndex >= 0) {
      this.stagedTags.splice(tagIndex, 1);
    }
  }

  @Mutation
  public cancelAddingPost() {
    this.isEditing = false;
  }

  @Mutation
  public setEditionModalOpenState(newState: boolean) {
    this.isEditing = newState;
    this.isPristine = true;
  }
  @Mutation
  public setModalMode(newMode: ModalMode) {
    this.modalMode = newMode;
  }
  @Mutation
  public setModelDirty() {
    this.isPristine = false;
  }
}
