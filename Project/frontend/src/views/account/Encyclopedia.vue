<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container v-if="ready">
        <v-row class="mt-15 pt-10">
          <v-col cols="12" class="encyclopedia-subtitle py-0 font-weight-bold">{{userinfo.nickname}} 님의</v-col>
          <v-col cols="12" class="encyclopedia-title pt-0 font-weight-bold">수상한 동물도감</v-col>
        </v-row>
        <v-container class="pb-10">
          <v-row>
            <v-col cols="3" v-for="(animal, index) in myEncyclopedia" :key="index" class="px-1 py-1">
              <div v-if="animal.encyclopedia" @click="opendialog(animal, index)" class="d-flex justify-center">
                <v-card width="60" height="60" elevation="0" class="d-flex justify-center text-center">
                  <v-img :src="'/api'+animal.images[0]" alt="" height="100%" cover></v-img>
                </v-card>
              </div>
              <div v-else @click="opendialog(animal, index)"  class="d-flex justify-center">
                <v-card width="60" height="60" color="grey lighten-2" elevation="0" class="grey--text font-weight-bold text--darken-1 align-center d-flex justify-center">
                  ?
                </v-card>
              </div>
              <div class="text-caption mt-1">
                No. {{index}}
              </div>
            </v-col>
          </v-row>
        </v-container>
        <!-- <v-row class="justify-end mr-3 mt-3">
          <router-link to="/history" class="text-decoration-none grey--text"><v-icon small class="mr-1">mdi-clock</v-icon>분석 히스토리</router-link>
        </v-row> -->
      </v-container>
      <v-container v-else class="pt-15">
        <v-col cols="12" class="grey--text py-0">도감 정보를</v-col>
        <v-col cols="12" class="grey--text pt-0 pb-5">불러오고있습니다</v-col>
        <v-col cols="12" class="grey--text py-0">잠시만 기다려주세요</v-col>
        <v-col cols="12" class="px-0">
        <v-progress-linear color="grey" indeterminate rounded height="6" class="px-15"></v-progress-linear>
        </v-col>
      </v-container>
    </div>
    <v-dialog v-model="dialog" width="300">
      <v-card class="py-5">
        <FoundModal v-if="selectedAnimal.encyclopedia" class="px-5 py-5" :selectedAnimal="selectedAnimal" :selectedAnimalPK="selectedAnimalPK"/>
        <NotFoundModal v-else class="px-5 py-5" :selectedAnimal="selectedAnimal" :selectedAnimalPK="selectedAnimalPK"/>
        <div class="d-flex justify-center">
        <router-link :to="{ path: '/animal/detail', query: {number:selectedAnimalPK} }" class="text-decoration-none dialog-guide">
          <v-btn color="#8A0000 " text class="dialog-guide">
          동물 정보
          </v-btn>
        </router-link>
        <v-btn color="grey" text @click="dialog = false" class="dialog-guide">
          닫기
        </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'

import { mapGetters } from 'vuex'

import FoundModal from '../../components/account/FoundModal.vue'
import NotFoundModal from '../../components/account/NotFoundModal.vue'

export default {
  name: 'encyclopedia',
  components: {
    FoundModal, NotFoundModal
  },
  data() {
    return {
      dialog: false,
      selectedAnimal: {},
      selectedAnimalPK : '',
      myEncyclopedia: {},
      ready: false,
    }
  },
  methods: {
    opendialog(a,i) {
      this.selectedAnimal = a
      this.selectedAnimalPK = i
      this.dialog = true
    },
  },
  created(){
    let config = {
      headers: {
        Authorization: `Token ${this.$cookies.get('auth-token')}`
      }
    }
    axios.get(SERVER.URL + SERVER.ROUTES.userinfo, config)
        .then(res => {
          this.$store.state.user = res.data
          let username = this.$store.state.user.username
          axios.get(SERVER.URL + SERVER.ROUTES.encyclopedia + `${username}/encyclopedia/`, config)
          .then(res => {
            this.myEncyclopedia = res.data
            this.ready = true
          })
        })
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'userinfo']),
  }
}
</script>

<style scoped>
.encyclopedia-title {
  color: #8A0000;
  font-size: 2.5rem;
}
.encyclopedia-subtitle {
  color: #8A0000;
  font-size: 1.5rem;
}
.encyclopedia-guide {
  font-size: x-large;
}
.button-word {
  font-size: large;
  width: 70%
}
.text-guide {
  color: #8A0000;
}
.dialog-guide {
  font-size: large;
}
</style>