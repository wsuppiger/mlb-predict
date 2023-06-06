import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PredictGameView from '../views/PredictGameView.vue'

const routes = [{
  path: '/',
  name: 'home',
  component: HomeView
},
{
  path: '/predictGame',
  name: 'predict game',
  // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  component: PredictGameView
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router