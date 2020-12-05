<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container class="d-flex flex-column justify-center text-center">
        <v-row class="pt-5">
          <v-col cols="12" class="home-subtitle py-0 mb-1 font-weight-bold">{{today}}</v-col>
          <v-col cols="12" class="home-title py-0 mb-1 font-weight-bold">동물 소개</v-col>
          <v-col cols="12" class="d-flex justify-center">
            <router-link :to="{ path: '/animal/detail', query: {number:todayAnimal.id} }" class="text-decoration-none">
            <v-card elevation="0" outlined width="80vw">
             <v-img height="200"
              :src="'/api'+todayAnimalImage"
              cover
            ></v-img> 
            <v-card-text class="pb-1">
              <div class="daily-title">{{todayAnimal.name}}</div>
              <div class="daily-subtitle">{{todayAnimal.english_name}}</div>
            </v-card-text>
            </v-card>
            </router-link>
          </v-col>
        </v-row>
        <!-- <v-divider class="mx-5 mt-5"></v-divider> -->
        <v-row class="pt-3 pb-5">
          <v-col cols="12" class="py-1 px-0">
            <router-link to="/findanimal" class="text-decoration-none">
            <v-card elevation="0" outlined width="80vw" class="mx-auto">
            <v-card-text>
              <div class="grey--text  mb-3 text-caption">AI로 동물 사진 분석하기</div>
              <div class="link-title">사진 으로 동물 분석</div>
            </v-card-text>
            </v-card>
            </router-link>            
          </v-col>
          <v-col cols="12" class="py-1 px-0 pt-3">
            <router-link to="/finduser" class="text-decoration-none">
            <v-card elevation="0" outlined width="80vw" class="mx-auto">
            <v-card-text>
              <div class="grey--text mb-3 text-caption gre">AI로 이목구비 분석하기</div>
              <div class="link-title">나와 닮은 동물 찾기</div>
            </v-card-text>
            </v-card>
            </router-link>            
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
  name: 'mainpage',
  data() {
    return {
      today:'',
      todayAnimal: '',
      todayAnimalImage: '/api/images/default.jpg'
    }
  },
  created() {
    var date = new Date(); 
    var year = date.getFullYear(); 
    var month = new String(date.getMonth()+1); 
    var day = new String(date.getDate()); 
    this.today = year +'.'+ month +'.'+ day

    axios.get(SERVER.URL + SERVER.ROUTES.today)
    .then(res => {
      this.todayAnimal = res.data
      this.todayAnimalImage = res.data.image_1
    })
  },
}
</script>

<style scoped>
.home-title {
  color: #8A0000;
  font-size: 2.5rem;
}
.home-subtitle {
  color: #8A0000;
  font-size: 1.3rem;
}
.daily-title {
  font-size: x-large;
  color: black;
  font-weight: 500;
}
.daily-subtitle {
  font-size: medium;
  color: rgb(190, 190, 190);
}
.link-title {
  font-size: x-large;
  color: black;
  font-weight: 600;
}
</style>