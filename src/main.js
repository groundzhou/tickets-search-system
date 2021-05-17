import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import { DatePicker, Select, Option, Loading } from 'element-ui';

import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'

axios.defaults.baseURL = 'http://localhost:5000'
Vue.config.productionTip = false
Vue.use(DatePicker)
Vue.use(Select)
Vue.use(Option)
Vue.use(Loading)
Vue.use(VueAxios, axios)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
