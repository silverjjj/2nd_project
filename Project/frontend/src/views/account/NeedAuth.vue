<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="auth-title py-0 mb-1 font-weight-bold">수상한</v-col>
          <v-col cols="12" class="auth-title py-0 font-weight-bold">동물사전</v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="py-1">
            <v-btn @click="kakaoLogin" class="button-word font-weight-bold">
            <!-- <a href="http://localhost:8000/api/accounts/kakao/login"> -->
              <v-img class="button-word mx-auto" src="@/assets/sns/kakao_login_medium_narrow.png"></v-img>
            <!-- </a> -->
            </v-btn>
          </v-col>
          <v-col cols="12" class="py-1">
            <router-link to="/login" class="text-decoration-none"><v-btn color="#8A0000" class="white--text button-word text-button"><v-icon class="mr-2">mdi-book-account</v-icon>일반 회원으로 로그인</v-btn></router-link>
          </v-col>
          <v-col cols="12" class="py-0 text-caption mt-1">
            아직 회원이 아니십니까?<router-link to="/signup" class="help-text text-decoration-none text-guide ml-3">회원가입</router-link>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'need-auth',
  methods: {
    kakaoLogin() {
      window.Kakao.Auth.login({
        success: this.GetMe,
      });
    },
    GetMe() {
      window.Kakao.API.request({
        url:'/v2/user/me',
        success : res => {
          const kakao_account = res.kakao_account
          const userInfo = {
            username : res.id,
            nickname : kakao_account.profile.nickname,
            email : kakao_account.email
          }
          axios.post(SERVER.URL + '/api/accounts/social_signup/', userInfo)
            .then(res => {
              if (res.data.message) {
                this.$store.state.authToken = res.data.token
                this.$cookies.set('auth-token', res.data.token)
                this.$store.state.user = res.data.user 
                this.$router.push('/guide')
              } else if (res.data.new) {
                this.$router.push({name: 'Socialsignup', params: res.data.new})
              } else {
                alert(res.data.error)
              }
            })
        }
      })
    },
  },
}
</script>

<style scoped>
.auth-title {
  color: #8A0000;
  font-size: 3rem;
}
.auth-guide {
  font-size: x-large;
}
.button-word {
  font-size: large;
  width: 222px;
  height: 49px !important;
}
.text-guide {
  color: #8A0000;
}
</style>