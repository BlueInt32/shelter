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
import { SaveElementApiModel } from '@/objects/apiModels/SaveElementApiModel';

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
@Module({ dynamic: true, namespaced: true, name: 'menu', store })
export default class Menu extends VuexModule {
  public isMenuOpen: boolean = false;
  @Mutation
  public setMenuOpenState(newState: boolean) {
    this.isMenuOpen = newState;
  }
}
