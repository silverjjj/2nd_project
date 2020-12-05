import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/home/Home.vue'
import GuidePage from '../views/home/GuidePage.vue'

import NeedAuth from '../views/account/NeedAuth.vue'
import FindAuth from '../views/account/FindAuth.vue'
import Login from '../views/account/Login.vue'
import Signup from '../views/account/Signup.vue'
import MyPage from '../views/account/MyPage.vue'
import Profile from '../views/account/Profile.vue'
import Encyclopedia from '../views/account/Encyclopedia.vue'
import SocialSignup from '../views/account/SocialSignup.vue'

import FindAnimal from '../views/analysis/AnimalAnalysis.vue'
import FindUser from '../views/analysis/UserAnalysis.vue'

import Search from '../views/animal/AnimalMain.vue'
import AnimalDetail from '../views/animal/AnimalDetail.vue'

import ErrorPage from '../views/else/Error.vue'
import ServerErrorPage from '../views/else/ServerError.vue'
import CheckPage from '../views/else/Check.vue'

import store from '../store/index'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/guide',
    name: 'GuidePage',
    component: GuidePage
  },
  {
    path: '/auth',
    name: 'NeedAuth',
    component: NeedAuth,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === true) {
        alert('이미 로그인 한 상태입니다.')
        next('/guide')
      } else {
        next()
      }
    }
  },
  {
    path: '/find-auth',
    name: 'FindAuth',
    component: FindAuth,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === true) {
        alert('이미 로그인 한 상태입니다.')
        next('/guide')
      } else {
        next()
      }
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === true) {
        alert('이미 로그인 한 상태입니다.')
        next('/guide')
      } else {
        next()
      }
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === true) {
        alert('이미 로그인 한 상태입니다.')
        next('/guide')
      } else {
        next()
      }
    }
  },
  {
    path: '/socialsignup',
    name: 'Socialsignup',
    component: SocialSignup,
    props: true,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === true) {
        alert('이미 로그인 한 상태입니다.')
        next('/guide')
      } else {
        next()
      }
    }
  },
  {
    path: '/mypage',
    name: 'MyPage',
    component: MyPage,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === false) {
        next('/check')
      } else {
        next()
      }
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === false) {
        next('/check')
      } else {
        next()
      }
    }
  },
  {
    path: '/encyclopedia',
    name: 'Encyclopedia',
    component: Encyclopedia,
    beforeEnter(from, to, next) {
      if (!store.state.authToken) {
        next('/check')
      } else {
        next()
      }
    }
  },
  {
    path: '/findanimal',
    name: 'FindAnimal',
    component: FindAnimal
  },
  {
    path: '/finduser',
    name: 'Finduser',
    component: FindUser
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/animal/detail',
    name: 'AnimalDetail',
    component: AnimalDetail
  },
  {
    path: '/error',
    name: 'ErrorPage',
    component: ErrorPage
  },
  {
    path: '/server/error',
    name: 'ServerErrorPage',
    component: ServerErrorPage
  },
  {
    path: '/check',
    name: 'CheckPage',
    component: CheckPage,
    beforeEnter(from, to, next) {
      if ( store.getters.isLoggedIn === true) {
        alert('이미 로그인 한 상태입니다.')
        next('/guide')
      } else {
        next()
      }
    }
  },
  {
    path: '*',
    redirect: '/error',
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
