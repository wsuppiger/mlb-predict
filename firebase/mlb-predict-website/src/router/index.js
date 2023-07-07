import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import PredictGameView from '../views/PredictGameView.vue'

const routes = [{
  path: '/',
  name: 'home',
  component: HomeView
},
{
  path: '/about',
  name: 'About',
  component: AboutView
},
{
  path: '/predict-game/:date/:gamePk',
  name: 'Predict Game',
  // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  component: PredictGameView
}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router