import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    gemsCategories: [
      {
        id: 1,
        title: 'general'
      },
      {
        id: 2,
        title: 'sound design'
      }
    ]
  },
  mutations: {},
  actions: {},
  modules: {}
});
