import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';


const KAKAO_KEY = process.env.VUE_APP_KAKAO_KEY
window.Kakao.init(KAKAO_KEY)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
