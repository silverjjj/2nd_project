<template>
  <v-app class="entire-page">
    <div class="inner-page rounded-xl">
      <v-app-bar
        color="transparent"
        dense
        fixed
        elevation="0"
        v-if="!isfirstpage"
      >
        <v-btn icon @click.stop="drawer = !drawer" class="ml-1">
          <img src="@/assets/icon/bookmark.png" width="80" alt="bookmark">
        </v-btn>
        <v-spacer></v-spacer>
      </v-app-bar>
      <v-navigation-drawer
        v-model="drawer"
        temporary
        app
        color="#8A0000"
        class="rounded-r-xl"
      >
        <v-container class="nav-drawer d-flex flex-column justify-center align-center">
          <v-container class="text-center">
            <v-row justify="center" class="white--text">
              <v-col cols="12"><img src="@/assets/icon/key.png" alt="cat-icon" width="30%"></v-col>
              <v-col cols="12" class="nav-userhi mt-1 py-0">안녕하세요,</v-col>
              <v-col v-if="isLoggedIn" cols="12" class="white--text nav-username py-0 mb-4">{{userinfo.nickname}} <span class="white--text">님</span></v-col>
              <v-col v-else cols="12" class="white--text nav-username py-0 mb-4">방문자 <span class="white--text">님</span></v-col>
            </v-row>
            <v-divider class="mx-5 mt-5 white"></v-divider>
            <v-row justify="center">
              <router-link to="/guide" class="nav-link text-decoration-none white--text py-1 my-2">홈 / 동물 분석</router-link>
            </v-row>
            <v-divider class="mx-5 white"></v-divider>
            <v-row justify="center">
              <router-link to="/search" class="nav-link text-decoration-none white--text my-2 py-1">동물 검색</router-link>
            </v-row>
            <v-divider class="mx-5 white"></v-divider>
            <v-row justify="center">
              <router-link to="/encyclopedia" class="nav-link text-decoration-none white--text my-2 py-1">동물 도감</router-link>
            </v-row>
            <v-divider class="mx-5 white"></v-divider>
            <v-row v-if="isLoggedIn" justify="end" class="mt-5 mx-5 white--text">
              <router-link to="/mypage" class="text-decoration-none white--text">
                <v-icon small class="mr-1 white--text">mdi-cog-outline</v-icon> 나의 계정
              </router-link>
              <!-- <v-icon small class="mr-2 white--text">mdi-account-arrow-right-outline</v-icon> 로그아웃 -->
            </v-row>
            <v-row v-else justify="end" class="mt-5 mx-5 white--text">
              <router-link to="/auth" class="text-decoration-none white--text">
              <v-icon small class="mr-1 white--text">mdi-account</v-icon> 로그인
              </router-link>
            </v-row>
          </v-container>
        </v-container>
      </v-navigation-drawer>

      <div v-if="isfirstpage" class="entrance d-flex justify-center align-center">
        <div>
            <v-row class="text-center">
              <!-- <v-col cols="12" class=" animate__animated animate__zoomIn animate__slow">
                <img src="@/assets/main/title.png" alt="logo cat" width="300">
              </v-col> -->
                <v-col cols="12" class="main-title py-0 mb-1 animate__animated animate__zoomIn animate__slow">수상한</v-col>
                <v-col cols="12" class="main-title py-0 animate__animated animate__zoomIn animate__slow">동물사전</v-col>    
                <v-col cols="12" class="sub-title py-0 mt-2 animate__animated animate__zoomIn animate__slow">Strange Encyclopedia</v-col>         
            </v-row>
        </div>
      </div>
      
      <router-view v-else class="content-page"/>
    </div>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'

import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'App',
  components: {

  },
  data() {
    return {
      isfirstpage: true,
      drawer: null,
    }
  },
  created() {
    // 첫 화면 - 임시로 set time out 설정해 주었음
    if (sessionStorage.visit) {
      this.isfirstpage = false
    } else {
      sessionStorage.setItem('visit', 1)
    }
    setTimeout(() => {
      this.isfirstpage = false
    }, 2000)

    axios.get(SERVER.URL + SERVER.ROUTES.animals)
    .then(res => {
      this.$store.state.animals = res.data
    })

    if (this.$store.state.authToken) {
      const config = {
      headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      } 
      axios.get(SERVER.URL + SERVER.ROUTES.userinfo, config)
        .then(res => {
          this.$store.state.user = res.data
        })
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'userinfo']),
  }
}
</script>
<style>
.entire-page {
  font-family: 'YiSunShinRegular', sans-serif !important;
  background-color: #8A0000 !important;
}
.inner-page {
  background-color: white;
  margin: 8px 8px;
  height: 100%;
}
.entrance {
  background-color:  #8A0000;
  background-image: url('../src/assets/main/outline.png');
  background-blend-mode: multiply;
  background-size: 98% 98%;
  background-position: center;
  background-attachment: fixed;
  width: 100%;
  height: 100%;
  z-index: 8;
}
.main-title {
  color: #F4B183;
  font-size: 3rem;
}
.sub-title {
  color: #F4B183;
  font-size: large;
  letter-spacing: 1px;
}
.content-page {
  height: 100%;
}
.bottom-nav {
  box-shadow: none !important;
  max-width: 100vw;
}
.menu {
  width: 20%;
}
.menu-btn {
  height: 100% !important;
}
.nav-drawer {
  height: 100%;
}
.nav-username {
  font-size: xx-large;
}
.nav-userhi {
  font-size: large;
}
.nav-link {
  font-size: larger;
}
.v-application ul, .v-application ol {
  padding-left: 0 !important;
}
</style>