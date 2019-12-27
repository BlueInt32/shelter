import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import Snotify, { SnotifyPosition } from 'vue-snotify';

Vue.config.productionTip = false;
const snotifyOptions = {
  toast: {
    position: SnotifyPosition.rightTop
  }
};
Vue.use(Snotify, snotifyOptions);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
