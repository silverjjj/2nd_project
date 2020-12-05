<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="signup-title py-0 font-weight-bold">회원가입</v-col>
        </v-row>
        <v-row class="mt-10">
          <v-col cols="12" class="py-0">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="닉네임"
            placeholder=" "
            color="#8A0000"
            v-model="nickname"
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
          <v-col cols="12" class="py-0">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="비밀번호"
            placeholder=" "
            color="#8A0000"
            type="password"
            v-model="SignupData.password1"
          ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-0">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="비밀번호 확인"
            placeholder=" "
            color="#8A0000"
            type="password"
            v-model="SignupData.password2"
          ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-btn @click="signup(SignupData)" outlined color="#8A0000" class="button-word font-weight-bold">회원가입</v-btn>
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
import { mapActions } from 'vuex'
import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'sign-up',
  data() {
    return {
      nickname: '',
      SignupData: {
        email: '',
        password1: '',
        password2: '',
        nickname: '',
        confirmed: false,
      },
      check: '닉네임 중복확인',
    }
  },
  methods: {
    ...mapActions(['signup']),
    nicknameCheck() {
      if (this.nickname === '') {
        alert('닉네임을 입력해주세요')
      } else {
        const params = {
            nickname : this.nickname
        }
        axios.get(SERVER.URL + '/api/accounts/signup/', {params})
          .then(res => {
            if (res.data.error) {
                this.check = '이미 존재하는 닉네임 입니다.'
                this.SignupData.confirmed = false
            } else {
                this.check = '사용 가능한 닉네임 입니다'
              this.SignupData.nickname = this.nickname
              this.SignupData.confirmed = true
            }
        })
      }
    }
  },
  watch: {
    nickname() {
      this.check = '닉네임 중복 확인'
      this.SignupData.confirmed = false
    }
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