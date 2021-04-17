import Vue from 'vue'
import Router from 'vue-router'

import HomePage from '../docs/HomePage'
import TicketsPage from "../docs/categories/TicketsPage";
import ComponentsPage from "../docs/categories/ComponentsPage";
import AdvancedPage from "../docs/categories/AdvancedPage";

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
      path: '/components',
      name: 'ComponentsPage',
      component: ComponentsPage
    }, {
      path: '/advanced',
      name: 'AdvancedPage',
      component: AdvancedPage
    },]
})
