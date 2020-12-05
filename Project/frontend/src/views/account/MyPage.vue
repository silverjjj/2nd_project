<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="mypage-subtitle py-0 font-weight-bold">안녕하세요,</v-col>
          <v-col cols="12" class="mypage-title py-0 font-weight-bold">{{userinfo.nickname}} 님</v-col>
        </v-row>
        <v-row class="mt-5 pb-0">
          <v-col cols="12" class="py-0">
            <div><img src="@/assets/account/cameraman.png" alt="" width="30%"></div>
          </v-col>
        </v-row>
        <v-divider class="mx-10 mt-n4 black"></v-divider>
        <v-row>
          <v-col cols="12">
            <v-col cols="12" class="mypage-subtitle py-0 font-weight-bold">내가 발견한 동물</v-col>
            <v-col cols="12" class="mypage-subtitle py-0 font-weight-bold">{{userinfo.total_ency}} / 100</v-col>
          </v-col>
        </v-row>
        <v-divider class="mx-10 black"></v-divider>
        <v-row>
          <v-col cols="12" class="text-caption">
            <router-link to="/profile" class="text-decoration-none grey--text mr-5">회원정보</router-link>
            | <router-link to="/encyclopedia" class="text-decoration-none text-guide ml-5">나의 동물 도감</router-link>
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
  name: 'mypage',
  computed: {
    userinfo() {
      return this.$store.state.user
    }
  },
  created() {
    const config = {
      headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
    } 
    if (this.$store.state.authToken) {
      axios.get(SERVER.URL + SERVER.ROUTES.userinfo, config)
        .then(res => {
          this.$store.state.user = res.data
        })
    }
  }
}
</script>

<style scoped>
.mypage-title {
  color: black;
  font-size: 2.5rem;
}
.mypage-subtitle {
  color: black;
  font-size: 1.5rem;
}
.mypage-guide {
  font-size: x-large;
}
.button-word {
  font-size: large;
  width: 70%
}
.text-guide {
  color: #8A0000;
}

</style>