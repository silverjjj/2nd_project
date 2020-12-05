<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="auth-subtitle py-0 font-weight-bold">아이디, 비밀번호</v-col>
          <v-col cols="12" class="auth-title py-0 font-weight-bold">조회하기</v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="py-1">
            <v-btn @click.stop="IDdialog = true" outlined color="#8A0000" class="button-word font-weight-bold">아이디 찾기</v-btn>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-btn @click.stop="PWdialog = true" outlined color="#8A0000" class="button-word font-weight-bold">비밀번호 재발급</v-btn>
          </v-col>
          <v-col cols="12" class="text-caption">
            <router-link to="/login" class="text-decoration-none grey--text">돌아가기</router-link>          </v-col>
        </v-row>
      </v-container>
    </div>
    <v-dialog v-model="IDdialog" width="300">
      <v-card>
        <v-card-title class="font-weight-bold justify-center">아이디 찾기</v-card-title>
        <v-card-text>
          <div v-if="!IDclicked">
            <div class="text-center">회원가입 시 입력한 닉네임을 입력해주세요</div>
            <v-text-field
              v-model="findEmail"
              color="#8A0000"
              required
              class="px-5"
            ></v-text-field>
          </div>
          <div v-else>
            <div class="text-center text-caption mt-3">회원님의 아이디는</div>
            <div class="text-center text-caption">'{{resultemail}}' 입니다.</div>
          </div>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn v-if="!IDclicked" @click="IDcheck" color="#8A0000" text>아이디 찾기</v-btn>
          <v-btn color="grey" text @click="IDclose">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="PWdialog" width="300">
      <v-card>
        <v-card-title class="font-weight-bold justify-center">비밀번호 재발급</v-card-title>
        <v-card-text>
          <div v-if="!PWclicked" class="pt-5">
            <div class="text-center">이메일을 입력해주세요</div>
            <v-text-field
              v-model="userData.email"
              color="#8A0000"
              required
              class="px-5 pt-0"
            ></v-text-field>
          </div>
          <div v-if="!PWclicked">
            <div class="text-center pt-5">닉네임을 입력해주세요</div>
            <v-text-field
              v-model="userData.nickname"
              color="#8A0000"
              required
              class="px-5 pt-0"
            ></v-text-field>
          </div>
          <div v-else>
            <div class="text-center text-caption mt-3">회원님의 이메일로</div>
            <div class="text-center text-caption">새로운 비밀번호가 발급되었습니다.</div>
          </div>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn v-if="!PWclicked" @click="PWcheck" color="#8A0000" text>재발급</v-btn>
          <v-btn color="grey" text @click="PWclose">닫기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'FindAuth',
  data() {
    return {
      IDdialog: false,
      findEmail: '',
      IDclicked: false,
      resultemail: 'ssafy@naver.com',
      PWdialog: false,
      email: '',
      PWclicked: false,
      userData: {
        email: '',
        nickname: '',
      },
    }
  },
  methods: {
    IDclose() {
      this.findEmail = ''
      this.useremail = ''
      this.IDclicked = false
      this.IDdialog = false
    },
    IDcheck() {
      if (this.findEmail === '') {
        alert ('닉네임을 입력해주세요')
      } else {
        axios.get(SERVER.URL + `/api/accounts/${this.findEmail}/find_id/`)
        .then(res => {
          if (res.data.message==="Error") {
            alert('회원 정보를 찾을 수 없습니다.')
          } else {
            if (res.data.login_method) {
              alert(res.data.login_method)
            } else {
              this.resultemail = res.data.email
              this.IDclicked = true
            }
          }
        })
        this.findEmail = ''
      }
    },
    PWclose() {
      this.userData.email = ''
      this.userData.nickname = ''
      this.PWclicked = false
      this.PWdialog = false
    },
    PWcheck() {
      if (this.userData.email.trim() === ''||this.userData.nickname.trim()==='') {
        alert ('모든 항목을 입력해주세요')
      } else {
        const params = this.userData
        axios.get(SERVER.URL + '/api/accounts/change_pw/', { params })
        .then(res => {
          if (res.data.message) {
            alert(res.data.message)
          } else {
            this.PWclick = true
            if (res.data.error) {
              alert('에러가 발생했습니다. 다시 시도해주세요')
            } else {
              this.userData.email = ''
              this.userData.nickname = ''
              this.PWclicked = true
            }
          }
        })
      }
    },
  }
}
</script>

<style scoped>
.auth-title {
  color: #8A0000;
  font-size: 3rem;
}
.auth-subtitle {
  color: #8A0000;
  font-size: 1.5rem;
}
.login-guide {
  font-size: x-large;
}
.button-word {
  font-size: large;
  width: 70%
}
</style>