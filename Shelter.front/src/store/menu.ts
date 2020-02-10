import store from '.';
import {
  VuexModule,
  Module,
  Action,
  getModule,
  Mutation
} from 'vuex-module-decorators';

@Module({ dynamic: true, namespaced: true, name: 'menu', store })
export default class Menu extends VuexModule {
  public isMenuOpen: boolean = false;
  @Mutation
  public setMenuOpenState(newState: boolean) {
    this.isMenuOpen = newState;
  }
}
