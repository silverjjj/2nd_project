<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="signup-title py-0 font-weight-bold">회원정보</v-col>
        </v-row>
        <v-row class="mt-10">
          <v-col cols="12" class="py-0">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="닉네임"
            placeholder=" "
            color="#8A0000"
            v-model="c_nickname"
          ></v-text-field>
          </v-col>
          <v-col style="cursor: pointer; z-index:5;" cols="12" @click="nicknameCheck" class="pb-5 text-center red--text text--darken-3 text-caption mt-n6">
            {{check}}
          </v-col>
          <v-col cols="12" class="py-0">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="이메일"
            placeholder=" "
            color="#8A0000"
            v-model="SignupData.email"
          ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-btn @click="socialSignup(SignupData)" outlined color="#8A0000" class="button-word font-weight-bold">회원정보입력</v-btn>
          </v-col>
          <v-col cols="12" class="text-caption">
            이미 회원이십니까? <router-link to="/login" class="text-guide text-decoration-none ml-3">로그인</router-link>
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
  name: 'social-sign-up',
  props: {
    username: {
      type: String,
      default: ''
    },
    nickname: {
      type: String,
      default: ''
    },
    email: {
      type: String,
      default: ''
    },
  },
  data() {
    return {
      c_nickname: '',
      SignupData: {
        email: '',
        nickname: '',
        confirmed: false,
      },
      check: '닉네임 중복확인',
    }
  },
  methods: {
      setCookies(Token) {
      this.$store.state.authToken = Token
      this.$cookies.set('auth-token', Token)
      this.IsLoggedIn = true
      },
      socialSignup(SignupData) {
      if (!SignupData.nickname.trim()||!SignupData.email.trim()) {
        alert('모든 항목을 입력해주세요')
      } else if (SignupData.confirmed === false) {
        alert('닉네임 중복 여부를 확인해주세요')
      } else if (!/.+@.+\..+/.test(SignupData.email)) {
        alert('이메일 형식에 맞게 입력해주세요')
      } else {
        const SignupData2 = {
          username: this.$route.params.username,
          email: SignupData.email,
          nickname: SignupData.nickname
        }
        axios.post(SERVER.URL + '/api/accounts/new_kakao/', SignupData2)
        .then(res => {
          if (res.data.error) {
            alert(res.data.error.username||res.data.error.message)
          } else {
            alert('성공적으로 회원가입되었습니다.')
            this.setCookies(res.data.token)
            this.$store.state.user = res.data.user
            this.$router.push('/guide')
          }
        })
      }
    },
    nicknameCheck() {
      if (this.c_nickname === '') {
        alert('닉네임을 입력해주세요')
      } else {
        const params = {
          // email : this.SignupData.email,
          nickname : this.c_nickname,
        }
        axios.get(SERVER.URL + '/api/accounts/signup/', { params })
          .then(res => {
            if (res.data.error) {
              this.check = '이미 존재하는 닉네임 입니다'
              this.SignupData.confirmed = false
            } else {
              this.check = '사용 가능한 닉네임 입니다'
              this.SignupData.nickname = this.c_nickname
              this.SignupData.confirmed = true
            }
          })
      }
    }
  },
  watch: {
    c_nickname() {
      this.check = '닉네임 중복 확인'
      this.SignupData.confirmed = false
    }
  },
  created() {
    this.c_nickname = this.$route.params.nickname
    this.SignupData.email = this.$route.params.email
  }
}
</script>

<style scoped>
.signup-title {
  color: #8A0000;
  font-size: 3rem;
}
.button-word {
  font-size: large;
  width: 70%
}
.text-guide {
  color: #8A0000;
}
.input-control {
  width: 70%;
}
</style>