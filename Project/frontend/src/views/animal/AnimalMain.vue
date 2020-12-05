<template>
  <div class="d-flex justify-center align-center text-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container v-if="!isloading">
        <v-row v-if="!searched">
          <v-col cols="12" class="search-title py-0 font-weight-bold">동물 검색</v-col>
          <v-col cols="12" class="px-10">
            <v-text-field
              placeholder=" "
              rounded
              dense
              outlined
              color="#8A0000"
              append-outer-icon="mdi-magnify"
              @click:append-outer="clicked"
              @keyup.enter="clicked"
              v-model="searchword"
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="mt-n10 d-flex justify-center">
            <v-switch dense color="#8A0000" v-model="name" label="이름" class="mr-10"></v-switch>
            <v-switch dense color="#8A0000" v-model="content" label="내용"></v-switch>
          </v-col>
        </v-row>
        <v-row v-else class="pt-10">
          <div v-if="result.length>=1">
            <v-col cols="12" class="py-0 mb-5">
              '{{searchword}}'에 대한 검색결과입니다
            </v-col>
            <v-col cols="12" v-for="(r, index) in result" :key="index" class="px-5 py-1">
              <router-link :to="{ path: '/animal/detail', query: {number:r.id} }" class="text-decoration-none">
                <v-card class="mx-auto py-2" outlined >
                <v-list-item>
                  <v-card  width="100" elevation="0" class="d-flex justify-center align-center"><v-img :src="'/api' + r.image_1" :alt="r.name" height="80" cover></v-img></v-card>
                  <v-list-item-content class="py-0">
                    <div class="text-caption text-left ml-4 grey--text">No.{{r.id}}</div>
                    <v-list-item-title class="animal-name ml-4">{{r.name}}</v-list-item-title>
                    <v-list-item-subtitle class="animal-ename grey--text ml-4">{{r.english_name}}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                </v-card>
              </router-link>
              </v-col>
              <v-col cols="12" @click="reset" class="pt-5 text-guide">다시 검색하기</v-col>
            </div>
            <div v-else>
              <v-col cols="12" class="py-0">
                '{{searchword}}'에 대한 검색결과가 없습니다.
              </v-col>
              <v-col cols="12" @click="reset" class="pt-1 text-guide">다시 검색하기</v-col>
            </div>
        </v-row>
      </v-container>
      <v-container v-else class="px-0 load-container">
        <v-row class="px-0">
          <v-col cols="12" class="grey--text">검색중입니다</v-col>
          <v-col cols="12" class="px-0">
            <v-progress-linear color="grey" indeterminate rounded height="6"></v-progress-linear>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <v-snackbar v-model="snackbar" :timeout="timeout" color="#8A0000" bottom class="pb-3">
      <div class="text-center mx-auto snackbar-content">{{text}}</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
          <v-icon small>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'search-main',
  data() {
    return {
      name: true,
      content: false,
      searched: false,
      searchword: '',
      isloading: false,
      snackbar: false,
      text: '',
      timeout: 1500,
      result: [],
    }
  },
  methods: {
    clicked() {
      if (this.searchword.trim() === '') {
        this.snackbar = true
        this.text = '검색어를 입력해주세요'
      } else if (this.name===false&&this.content===false) {
        this.snackbar = true
        this.text = '검색 조건을 선택해주세요'
      }
      else {
        this.isloading = true
        if (this.name === false) {
          this.name = ''
        } else {
          this.name = this.searchword
        }
        if (this.content === false) {
          this.content = ''
        } else {
          this.content = this.searchword
        }
        axios.get(SERVER.URL + SERVER.ROUTES.animals, {
          params: {
            name: this.name,
            content: this.content,
          }
        })
            .then(res => {
              this.isloading = false
              this.searched = true
              this.result = res.data
            })
      }
    },
    reset() {
      this.searched = false
      this.searchword = ''
      this.name = true
      this.content = false
    }
  }
}
</script>

<style scoped>
.search-title {
  color: #8A0000;
  font-size: 3rem;
}
.search-guide {
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
.snackbar-content {
  font-size: large;
}
.load-container {
  width: 35vw;
}
.animal-name {
  font-size: x-large;
}
.animal-ename {
  font-size: medium;
}
</style>