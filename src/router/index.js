import Vue from 'vue'
import Router from 'vue-router'

import HomePage from '../pages/HomePage'
import TicketsPage from "../pages/TicketsPage";
import PricesPage from "../pages/PricesPage"
import CitiesPage from "../pages/CitiesPage"

Vue.use(Router)

export default new Router({
    scrollBehavior() {
        return {x: 0, y: 0}
    },
    routes: [{
        path: '/',
        name: 'Home',
        component: HomePage
    }, {
      path: '/tickets',
      name: 'TicketsPage',
      component: TicketsPage
    }, {
      path: '/prices',
      name: 'PricesPage',
      component: PricesPage
    }, {
      path: '/cities',
      name: 'CitiesPage',
      component: CitiesPage
    },]
})
