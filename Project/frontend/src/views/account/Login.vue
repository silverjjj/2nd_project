<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="login-title py-0 font-weight-bold">로그인</v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="이메일"
            placeholder=" "
            color="#8A0000"
            v-model="LoginData.username"
          ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-0">
            <v-text-field
            class="input-control mx-auto text-caption"
            label="비밀번호"
            placeholder=" "
            color="#8A0000"
            type="password"
            v-model="LoginData.password"
          ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-btn @click="login(LoginData)" outlined color="#8A0000" class="button-word font-weight-bold">로그인</v-btn>
          </v-col>
          <v-col cols="12" class="text-caption">
            <router-link to="/signup" class="text-decoration-none text-guide mr-5">회원가입</router-link>
            | <router-link to="/find-auth" class="text-decoration-none grey--text ml-5">ID/비밀번호 찾기</router-link>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'login',
  data() {
    return {
      LoginData: {
        username: '',
        password: '',
      },
    }
  },
  methods: {
    ...mapActions(['login'])
  }
}
</script>

<style scoped>
.login-title {
  color: #8A0000;
  font-size: 3rem;
}
.login-guide {
  font-size: x-large;
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