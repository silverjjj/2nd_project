<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="profile-subtitle py-0 font-weight-bold">{{userinfo.nickname}} 님의</v-col>
          <v-col cols="12" class="profile-title py-0 font-weight-bold">회원 정보</v-col>
        </v-row>
        <v-row class="pt-10 pb-1">
          <v-col cols="1"></v-col>
          <v-col cols="4" class="py-0 pr-0 pl-5 font-weight-bold">닉네임</v-col>
          <v-col cols="5" class="py-0 pl-0">{{userinfo.nickname}}</v-col>
          <v-col cols="1"></v-col>
        </v-row>
        <v-row class="pt-3 pb-7">
          <v-col cols="1"></v-col>
          <v-col cols="4" class="py-0 pr-0 pl-5 font-weight-bold">이메일</v-col>
          <v-col cols="5" class="py-0 pl-0">{{userinfo.email}}</v-col>
          <v-col cols="1"></v-col>
        </v-row>
        <v-row>
          <v-col cols="12" class="text-caption">
            <span class="text-guide mr-2" @click="OpenEdit">비밀번호 변경</span>
            | <span @click="logout" class="text-guide mx-2">로그아웃</span>
            | <span class="text-guide ml-2" @click.stop="ExitDialog = true">회원 탈퇴</span>
          </v-col>
          <v-col cols="12" class="mt-5"><router-link to="/mypage" class="text-caption text-decoration-none grey--text ml-2">마이 페이지로 돌아가기</router-link></v-col>
        </v-row>
      </v-container>
    </div>
    
    <v-dialog v-model="ExitDialog">
      <v-card>
        <v-card-title class="font-weight-bold d-flex justify-center modal-title py-10">회원 탈퇴</v-card-title>
        <v-card-text class="text-center text-subtitle-2 modal-info">
          모든 개인 정보와 도감이 
          <br> 삭제되어 복구할 수 없습니다. <br>
          <div class="mt-4">그래도 탈퇴를 진행하시겠습니까?</div>
        </v-card-text>
        <v-card-actions class="d-flex justify-center py-5">
          <v-btn color="#8A0000" text @click="WantExit" class="action-btn"> 네, 탈퇴하겠습니다</v-btn>
          <v-btn color="grey" text @click="ExitDialog = false" class="action-btn">돌아가기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="EditDialog">
      <v-card>
        <v-card-title class="font-weight-bold d-flex justify-center modal-title pt-10 pb-5">비밀번호 변경</v-card-title>
        <v-card-text class="text-center text-subtitle-2 modal-info pb-0">
          <v-container>
          <v-row class="mt-5">
            <v-col cols="12" class="py-0">
              <v-text-field
              class="input-control mx-auto text-caption"
              label="기존 비밀번호"
              v-model="newInfo.password"
              type="password"
              color="#8A0000"
            ></v-text-field>
            </v-col>
            <v-col cols="12" class="py-0">
              <v-text-field
              class="input-control mx-auto text-caption"
              label="새 비밀번호"
              v-model="newInfo.newpassword"
              type="password"
              color="#8A0000"
            ></v-text-field>
            </v-col>
            <v-col cols="12" class="py-0">
              <v-text-field
              class="input-control mx-auto text-caption"
              label="새 비밀번호 확인"
              v-model="newInfo.checkpassword"
              type="password"
              color="#8A0000"
            ></v-text-field>
            </v-col>
          </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="d-flex justify-center pb-5 ">
          <v-btn color="#8A0000" text @click="sendData" class="action-btn"> 수정하기</v-btn>
          <v-btn color="grey" text @click="CloseEdit" class="action-btn">돌아가기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar" :timeout="timeout" color="#8A0000" bottom class="pb-3">
      <div class="text-center mx-auto snackbar-content">{{text}}</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
          <v-icon small light class="white--text">mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'
import cookies from 'vue-cookies'

import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'user-profile',
  data() {
    return {
      ExitDialog: false,
      EditDialog: false,
      newInfo : {
        password: '',
        newpassword: '',
        checkpassword: '',
      },
      snackbar: false,
      text: '',
      timeout: 1500,
    }
  },
  methods: {
    ...mapActions(['logout']),
    OpenEdit() {
      if (this.$store.state.user.register_login_method==='email') {
        this.EditDialog = true
      } else {
        this.snackbar = true
        this.text = '소셜 회원은 비밀번호 수정이 불가합니다'
      }
    },
    CloseEdit() {
      this.newInfo.password = ''
      this.newInfo.newpassword = ''
      this.newInfo.checkpassword = ''
      this.EditDialog = false
    },
    WantExit() {
      let config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.delete(SERVER.URL + `/api/accounts/users/${this.$store.state.user.username}/me/`, config)
      .then(() => {
        alert('이용해주셔서 감사합니다.')
        cookies.remove('auth-token')
        this.$store.state.user = {}
        this.$router.push('/')
        this.$router.go(0)
      })
    },
    sendData() {
      if (this.newInfo.checkpassword.trim()===''||this.newInfo.password.trim()===''
      ||this.newInfo.newpassword.trim()===''){
        alert('모든 항목을 입력해주세요')
      } else if (this.newInfo.checkpassword.length<8||this.newInfo.newpassword.length<8){
        alert('비밀번호는 최소 8자 이상이어야 합니다.')
      } else if (this.newInfo.checkpassword !== this.newInfo.newpassword) {
        alert('비밀번호가 일치하지 않습니다')
      } else {
        let config = {
          headers: {
            Authorization: `Token ${this.$cookies.get('auth-token')}`
          }
        }
        axios.put(SERVER.URL + `/api/accounts/users/${this.$store.state.user.username}/me/`, this.newInfo, config)    
        .then(res => {
          if (res.data.error) {
            alert(res.data.error)
          } else {
            this.$store.state.user = res.data.user
            alert('성공적으로 변경되었습니다.')
            this.$router.go(0)
          }
        })   
      }
    },
  },
  computed: {
    ...mapGetters(['userinfo'])
  },
  created() {
    this.username = this.$store.state.user.nickname
    this.useremail = this.$store.state.user.email
  }
}
</script>

<style scoped>
.profile-title {
  color: black;
  font-size: 2.5rem;
}
.profile-subtitle {
  color: black;
  font-size: 1.5rem;
}
.button-word {
  font-size: large;
  width: 70%
}
.text-guide {
  color: #8A0000;
}
.modal-title {
  font-size: xx-large !important;
}
.modal-info {
  font-size: large;
}
.input-control {
  width: 90%;
}
.action-btn {
  font-size: medium;
}
</style>