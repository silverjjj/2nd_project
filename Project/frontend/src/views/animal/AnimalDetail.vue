<template>
  <div class="pt-15">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center text-caption">No. {{number}}</v-col>
          <v-col cols="12" class="detail-title py-0 font-weight-bold">{{animal.name}}</v-col>
          <v-col cols="12" class="detail-subtitle py-0 font-weight-bold">{{animal.english_name}}</v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12">
            <v-card class="mx-auto" max-width="344" elevation="0">
              <v-img :src="animal.image_1" contain alt="animal-picture" height="200px"></v-img>
            </v-card>
          </v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="text-left pl-7 char-subtitle">기본 정보</v-col>
          <v-col cols="12" class="px-5">
            <v-simple-table dense>
              <tbody>
                <tr><td class="d-title text-size py-2">학명</td> <td class="py-2">{{ animal.scientific_name }}</td></tr>
                <tr><td class="d-title text-size py-2">크기</td> <td class="py-2">{{ animal.avg_size }}</td></tr>
                <tr><td class="d-title text-size py-2">무게</td> <td class="py-2">{{ animal.avg_weight }}</td></tr>
                <tr><td class="d-title text-size py-2">분포지</td> <td class="py-2">{{ animal.distribution_area }}</td></tr>
              </tbody>
            </v-simple-table>
          </v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="text-left pl-7 char-subtitle">특징</v-col>
          <v-col cols="12" class="px-7 text-justify text-size2">
            {{animal.characteristics}}
          </v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="text-left pl-7 char-subtitle">이미지</v-col>
          <v-col cols="12" class="px-5">
            <v-container>
            <VueSlickCarousel v-bind="settings" class="mx-4">
              <v-card elevation="0" height="200" class="d-flex justify-center align-center">
                <v-img :src="animal.image_2" alt="" height="200" contain></v-img>
              </v-card>
              <v-card elevation="0" height="200" class="d-flex justify-center align-center">
                <v-img :src="animal.image_3" alt="" height="200" contain></v-img>
              </v-card>
              <v-card elevation="0" height="200" class="d-flex justify-center align-center">
                <v-img :src="animal.image_4" alt="" height="200" contain></v-img>
              </v-card>
              <v-card elevation="0" height="200" class="d-flex justify-center align-center">
                <v-img :src="animal.image_5" alt="" height="200" contain></v-img>
              </v-card>
            </VueSlickCarousel>
            </v-container>
          </v-col>
        </v-row>
        <v-row class="mt-10 pb-10">
          <v-col cols="12" class="text-left pl-7 char-subtitle">출처</v-col>
          <v-col cols="12" class="text-left pl-10">
            - 두산 백과, 구글 위키, 네이버 지식백과
          </v-col>
        </v-row>

        <v-row justify="center" class="grey--text" @click="toTop">
          상단으로 이동
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import VueSlickCarousel from 'vue-slick-carousel'
import 'vue-slick-carousel/dist/vue-slick-carousel.css'
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'

import axios from 'axios'
import SERVER from '@/api/drf.js'
import router from '@/router'

export default {
  name: 'animal-detail',
  components: {
    VueSlickCarousel
  },
  data() {
    return {
      number: this.$route.query.number,
      animals: [],
      animal: [],
      settings: {
        "dots": true,
        "focusOnSelect": true,
        "infinite": true,
        "speed": 500,
        "slidesToShow": 1,
        "slidesToScroll": 1,
        "touchThreshold": 3        
      }
    }
  },
  methods: {
    toTop() {
      window.scrollTo({ top: 0, behavior: 'smooth'})
    }
  },
  created() {
    window.scrollTo({top:0, behavior: 'smooth'})
    if (this.number>=1 && this.number<101) {
      axios.get(SERVER.URL + SERVER.ROUTES.animals)
      .then(res => {
        this.$store.state.animals = res.data
        this.animals = res.data
        this.animal = this.animals[this.number-1]
        this.animal.image_1 = '/api' + this.animal.image_1
        this.animal.image_2 = '/api' + this.animal.image_2
        this.animal.image_3 = '/api' + this.animal.image_3
        this.animal.image_4 = '/api' + this.animal.image_4
        this.animal.image_5 = '/api' + this.animal.image_5
      })
    } else {
      router.push('/error')
    }
  },
}
</script>

<style scoped>
.detail-title {
  color: black;
  font-size: 3rem;
}
.detail-subtitle {
  color:rgb(148, 148, 148);
  font-size: 1.5rem;
}
.char-subtitle {
  color: #8A0000;
  font-size: x-large;
  font-weight: bold;
}
.img-size {
  height: 200px !important;
}
.slick-dots {
  padding-left: 0 !important;
}
.d-title {
  width: 100px !important;
  padding-left: 10 !important;
  padding-right: 10 !important;
  font-weight: bold;
}
.text-size {
  font-size: large !important;
}
.text-size2 {
  font-size: medium !important;
}
</style>