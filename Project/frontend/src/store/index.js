import Vue from 'vue'
import Vuex from 'vuex'

import cookies from 'vue-cookies'
import router from '../router'
import axios from 'axios'

import SERVER from '@/api/drf.js'

Vue.use(Vuex)
Vue.use(cookies)

export default new Vuex.Store({
  state: {
    authToken: cookies.get('auth-token'),
    user: {},
    animals: {},
  },
  getters: {
    isLoggedIn: state => !!state.authToken,
    config: state => ({headers: {Authorization: `Token ${state.authToken}`}}),
    userinfo: state => state.user
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.authToken = token
      cookies.set('auth-token', token)
    },
    SET_USER(state, user) {
      state.user = user
    },
    REMOVE_TOKEN(state) {
      cookies.remove('auth-token')
      state.user = {}
      state.authToken = false
    },
  },
  actions: {
    login(context, LoginData) {
      if (!LoginData.username.trim()||!LoginData.password.trim()) {
        alert('모든 항목을 입력해주세요')
      } else if (!/.+@.+\..+/.test(LoginData.username)) {
        alert('이메일 형식으로 입력해주세요')
      } else {
        axios.post(SERVER.URL + SERVER.ROUTES.login, LoginData)
        .then(res => {
          if (res.data.error) {
            if (res.data.error.password) {
              if (res.data.error.message == 'Kakao') {
                alert(`${res.data.error.message} 로그인 계정입니다.`)
              } else if (res.data.error.message=='email') {
                alert(res.data.error.password)
              }
            } else if (res.data.error.username) {
              alert(res.data.error.username)
            }          } else {
            context.commit('SET_TOKEN', res.data.token)
            context.commit('SET_USER', res.data.user)
            router.push('/guide')
          }
        })
      }
    },
    signup(context, SignupData) {
      if (!SignupData.nickname.trim()||!SignupData.email.trim()
      ||!SignupData.password1.trim()
      ||!SignupData.password2.trim()) {
        alert('모든 항목을 입력해주세요')
      } else if (SignupData.confirmed === false) {
        alert('닉네임 중복 여부를 확인해주세요')
      } else if (!/.+@.+\..+/.test(SignupData.email)) {
        alert('이메일 형식에 맞게 입력해주세요')
      } else if (SignupData.password1 !== SignupData.password2) {
        alert('비밀번호가 일치하지 않습니다.')
      } else if (SignupData.password1.length < 8) {
        alert('비밀번호는 8자리 이상이어야 합니다')
      } else {
        const SignupData2 = {
          username: SignupData.email,
          email: SignupData.email,
          password: SignupData.password1,
          nickname: SignupData.nickname
        }
        axios.post(SERVER.URL + SERVER.ROUTES.signup, SignupData2)
        .then(res => {
          if (res.data.error) {
            alert(res.data.error.username||res.data.error.password||res.data.error.message)
          } else {
            alert('성공적으로 회원가입되었습니다.')
            context.commit('SET_TOKEN', res.data.token)
            context.commit('SET_USER', res.data.user)
            router.push('/guide')
          }
        })
      }
    },
    logout(context) {
      context.commit('REMOVE_TOKEN')
      context.commit('SET_USER', null)
      alert('성공적으로 로그아웃 되었습니다.')
      router.push('/guide')
    }
  },
  modules: {
  }
})
