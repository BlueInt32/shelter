import Vue from 'vue';
import Vuex from 'vuex';
import { GemCategoryViewModel } from '@/viewModels/GemCategoryViewModel';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    gemsCategories: [
      {
        id: 1,
        title: 'general'
      }
    ]
  },
  mutations: {},
  actions: {},
  modules: {}
});