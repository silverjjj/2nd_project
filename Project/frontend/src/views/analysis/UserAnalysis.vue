<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row v-if="!selected">
          <v-col cols="12" class="analysis-subtitle py-0 mb-1 font-weight-bold">AI 얼굴 분석</v-col>
          <v-col cols="12" class="analysis-title py-0 font-weight-bold">닮은 동물 찾기</v-col>
          <v-col cols="12" class="pt-0 mt-5">
            <v-btn outlined @click="onClickImageUpload" color="#8A0000" class="button-word2 font-weight-bold">
              <input ref="imageInput" type="file" hidden @change="onChangeImages">
              사진 선택
            </v-btn>
          </v-col>
        </v-row>
        <v-row v-else-if="!searched">
          <v-col cols="12" class="analysis-subtitle py-0 mb-1 font-weight-bold">AI 얼굴 분석</v-col>
          <v-col cols="12" class="analysis-title py-0 font-weight-bold">닮은 동물 찾기</v-col>
          <v-col cols="12" class="d-flex justify-center align-center my-3">
            <v-card max-width="300"  v-if="imageUrl">
              <v-img :src="imageUrl" width="300" height="300" cover @click="onClickImageUpload"></v-img>
              <input ref="imageInput" type="file" hidden @change="onChangeImages">
            </v-card>
            <v-card @click="onClickImageUpload" width="300" height="300" v-else color="grey lighten-2" elevation="0" class="d-flex justify-center align-center grey--text" >
              <input ref="imageInput" type="file" hidden @change="onChangeImages">
              이미지를 업로드 해주세요
            </v-card>  
          </v-col> 
          <v-col cols="12">
            <v-btn outlined color="#8A0000" class="button-word2 font-weight-bold" @click="nowclicked">검색하기</v-btn>
          </v-col>        
        </v-row>
        <v-row v-else-if="isloading">
          <v-col cols="12" class="grey--text">검색중입니다</v-col>
          <v-col cols="12" class="px-0">
            <v-progress-linear color="grey" indeterminate rounded height="6"></v-progress-linear>
          </v-col>
        </v-row>
        <v-row v-else>
          <v-carousel
            class="result-carousel"
            :show-arrows="false"
            hide-delimiter-background
            light
            style="height: 100%"
            >
            <v-carousel-item>
              <v-sheet color="transparent" height="100%">
                <v-row class="fill-height" align="center" justify="center">
                  <v-container>
                    <v-row>
                      <v-col cols="12" class="analysis-subtitle py-0 font-weight-bold">당신과 가장</v-col>
                      <v-col cols="12" class="analysis-subtitle py-0 mb-3 font-weight-bold">닮은 동물은 ...</v-col>
                      <v-col cols="12" class="analysis-new-title py-0 my-2 font-weight-bold">{{animal.name}}</v-col>
                      <v-col cols="12" class="d-flex justify-center align-center">
                        <v-card class="mx-1">
                          <v-img :src="imageUrl" width="130" height="130" cover></v-img>
                        </v-card>
                        <v-card class="mx-1">
                          <v-img :src="'/api'+animal.image_1" width="130" height="130" cover></v-img>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-row>
              </v-sheet>
            </v-carousel-item>
            <v-carousel-item>
              <v-sheet color="transparent" height="100%">
                <v-row class="fill-height" align="center" justify="center">
                  <v-container>
                    <v-row class="px-10">
                      <v-col cols="12">
                        이런 동물들과도 닮았어요!
                      </v-col>
                      <v-col cols="6"  v-for="(n,index) in options" :key="index" class="px-0 py-0">
                          <v-container class="d-flex justify-center align-center">
                          <v-card 
                          elevation="0"
                          width="150"
                          class="px-0 py-0 d-flex flex-column justify-center">
                              <v-img :src="'/api'+n.image_1" alt="" min-height="120" max-height="120" cover></v-img>
                            <div class="mt-3">{{n.name}}</div>
                          </v-card>
                          </v-container>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-row>
              </v-sheet>
            </v-carousel-item>
            <v-carousel-item>
                <v-sheet color="transparent" height="100%" width="100%" class="d-flex justify-center align-center">
                  <v-container class="d-flex flex-column justify-center align-center">
                  <v-row align="center" justify="center">
                    <v-col cols="12" class="pt-5">
                        <v-btn @click="reset" outlined color="#8A0000" class="button-word font-weight-bold"><v-icon class="mr-2">mdi-replay</v-icon> 다시 분석하기</v-btn>
                    </v-col>
                    <v-col cols="12" class="pt-2">
                      <router-link to="/guide" class="text-decoration-none">
                        <v-btn outlined color="#8A0000" class="button-word font-weight-bold"><v-icon class="mr-2">mdi-home</v-icon> 홈으로 돌아가기</v-btn>
                      </router-link>
                    </v-col>
                  </v-row>
                  </v-container>
                </v-sheet>
              </v-carousel-item>
          </v-carousel>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/drf.js'

export default {
  name: 'user-analysis',
  data() {
    return {
      selected: false,
      searched: false,
      isloading: false,
      imageUrl: '',
      encodedUrl: '',
      animal: {},
      options: {},
    }
  },
  methods: {
    nowclicked() {
      this.searched = true
      this.isloading = true
      const analysisData = {
        img_base64: this.encodedUrl
      }
      axios.post(SERVER.URL + SERVER.ROUTES.predict, analysisData)
        .then(res => {
          this.isloading = false
          var ele = []
          res.data.result.forEach(function(element) {
            ele.push(Object.values(element)[0])
          })
          var final = []
          for (var el of ele) {
            final.push(this.bringData(el))
          }
          this.animal = final[0]
          this.options = final.splice(1,5)
        })
    },
    bringData(name) {
      var animalList = this.$store.state.animals
      var temp = []
      animalList.forEach(function(element) {
        if (element.english_name === name) {
          temp = element
        }
      })
      return temp
    },
    reset() {
      this.selected = false
      this.searched = false
      this.isloading = false
      this.imageUrl = ''
    },
    onClickImageUpload() {
      this.selected = true
      this.$refs.imageInput.click()
    },
    onChangeImages(e) {
    const file = e.target.files[0]
    this.imageUrl = URL.createObjectURL(file)
    this.createBase64Image(file)
    },
    createBase64Image(fileObject) {
      const reader = new FileReader()
      reader.onload = (e) => {
        var tempUrl = e.target.result
        this.adjustEncodedUrl(tempUrl)
      }
      reader.readAsDataURL(fileObject)
    },
    adjustEncodedUrl(dataURL) {
      var strArray=dataURL.split(',')
      this.encodedUrl = strArray[1]
    },

  }
}
</script>

<style scoped>
.analysis-title {
  color: #8A0000;
  font-size: 2.5rem;
}
.analysis-new-title {
  color: black;
  font-size: 2.5rem;
}
.analysis-subtitle {
  color: #8A0000;
  font-size: 1.3rem;
}
.analysis-guide {
  font-size: x-large;
}
.button-word {
  font-size: large;
  width: 75%;
}
.button-word2 {
  font-size: large;
  width: 90%;
}
.result-carousel {
  padding-bottom: 10vh;
}
</style>