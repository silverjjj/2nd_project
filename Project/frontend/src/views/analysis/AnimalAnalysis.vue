<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row v-if="!selected">
          <v-col cols="12" class="analysis-subtitle py-0 mb-1 font-weight-bold">AI 동물 분석</v-col>
          <v-col cols="12" class="analysis-title py-0 font-weight-bold">동물 사진 분석</v-col>
          <v-col cols="12" class="pt-0 mt-5">
            <v-btn outlined @click="onClickImageUpload" color="#8A0000" class="button-word2 font-weight-bold">
              <input ref="imageInput" type="file" hidden @change="onChangeImages">
              사진 선택
            </v-btn>
          </v-col>
        </v-row>
        <v-row v-else-if="!searched">
          <v-col cols="12" class="analysis-subtitle py-0 mb-1 font-weight-bold">AI 동물 분석</v-col>
          <v-col cols="12" class="analysis-title py-0 font-weight-bold">동물 사진 분석</v-col>
          <v-col cols="12" class="d-flex justify-center align-center my-3">
            <v-card max-width="300" v-if="imageUrl" @click="onClickImageUpload" >
              <v-img :src="imageUrl" width="300" height="300" cover></v-img>
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
          <!-- <div class="result-page d-flex justify-center align-center"> -->
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
                        <v-col cols="12" class="analysis-subtitle py-0 font-weight-bold">사진과</v-col>
                        <v-col cols="12" class="analysis-subtitle py-0 mb-5 font-weight-bold">가장 닮은 동물은</v-col>
                        <v-col cols="12" class="analysis-new-title py-0 mb-5 font-weight-bold">'{{animal.name}}'</v-col>
                        <v-col cols="12" class="d-flex justify-center align-center">
                          <v-card class="mx-1">
                            <v-img :src="imageUrl" width="120" height="120" cover></v-img>
                          </v-card>
                          <v-card class="mx-1">
                            <v-img :src="'/api'+animal.image_1" width="120" height="120" cover></v-img>
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
                      <v-row>
                        <v-col cols="12" class="text-center analysis-subtitle black--text font-weight-bold pb-0">{{animal.name}}</v-col>
                        <v-col cols="12" class="d-flex justify-center align-center">
                          <v-card class="mx-1">
                            <v-img :src="'/api'+animal.image_2" width="200" height="200" cover></v-img>
                          </v-card>
                        </v-col>
                        <v-col cols="12" class="d-flex justify-center align-center px-15">
                          <v-simple-table dense>
                            <tbody>
                              <tr><td>동물</td> <td>{{animal.name}}</td></tr>
                              <tr><td>영문</td> <td>{{animal.english_name}}</td></tr>
                              <tr><td>학명</td> <td>{{animal.scientific_name}}</td></tr>
                            </tbody>
                          </v-simple-table>
                        </v-col>
                        <v-col cols="12">
                          <router-link :to="{ path: '/animal/detail', query: {number:animal.id} }" class="text-decoration-none text-guide">
                          {{animal.name}} 더 알아보기
                          </router-link>
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
                        <v-col cols="12" class="pb-5">
                          이런 동물들과도 닮았어요!
                        </v-col>
                        <v-col cols="6" v-for="(a,index) in options" :key="index" class="px-0 py-0">
                          <v-container class="d-flex justify-center align-center">
                          <v-card 
                          elevation="0"
                          width="150"
                          class="px-0 py-0 d-flex flex-column justify-center">
                            <div class="d-flex justify-center">
                              <v-img :src="'/api'+a.image_1" alt="" width="100%" height="130" cover></v-img>
                            </div>
                            <div class="mt-3 font-weight-bold adjust-text">{{a.name}}</div>
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
                    <v-col cols="12" class="mt-5" v-if="isLoggedIn">
                      <v-btn v-if="!registered" @click="register" color="#8A0000" class="button-word2 white--text font-weight-bold">도감등록</v-btn>
                      <v-btn v-else outlined disabled color="#8A0000" class="button-word2 red--text text--darken-3 font-weight-bold">도감 등록 완료</v-btn>
                    </v-col>
                    <v-col cols="12" class="pt-0">
                      <v-btn @click="reset" color="#8A0000" class="button-word2 white--text font-weight-bold">돌아가기</v-btn>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" class="grey--text" @click.stop="dialog = true">결과가 정확하지 않습니까?</v-col>
                  </v-row>
                  </v-container>
                </v-sheet>
              </v-carousel-item>
            </v-carousel>
          <!-- </div> -->
        </v-row>
      </v-container>
      <v-dialog v-model="dialog" width="300">
      <v-card>
        <v-card-title class="d-flex justify-center mb-3 font-weight-bold">피드백</v-card-title>
        <v-card-text class="d-flex justify-center align-center">
          <div>
            <div class="d-flex justify-center"><img :src="imageUrl" alt="input picture" width="200"></div>
            <div class="text-center mt-3">사진 속 동물의 이름을 입력해주세요</div>
            <div v-if="err" class="text-center text-guide">이름을 한 글자 이상 적어주세요</div>
            <div class="mt-2 px-3">
              <v-text-field
                placeholder=" "
                v-model="answer"
                outlined
                color="#8A0000"
                rounded
                dense
              ></v-text-field>
            </div>
          </div>
        </v-card-text>
        <v-card-actions class="d-flex justify-center mt-n10 pb-3">
          <v-btn color="#8A0000" text class="font-weight-bold btn-choice" @click="feedbackSubmit" >
            전송
          </v-btn>
          <v-btn color="grey" text class="font-weight-bold btn-choice" @click="dialog = false" >
            취소
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </div>
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

export default {
  name: 'animal-analysis',
  data() {
    return {
      selected: false,
      searched: false,
      isloading: false,
      imageUrl: '',
      encodedUrl: '',
      animal: {},
      options: [],
      registered: false,
      dialog: false,
      answer: '',
      err: false,
      snackbar: false,
      text: '검색어를 입력해주세요',
      timeout: 1500,
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
          this.isloading = false
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
      this.registered = false
      this.encodedUrl = ''
      this.animal = {}
      this.options = {}
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
    feedbackSubmit() {
      if (this.answer.trim() === '') {
        this.err = true
      } else {
        this.err = false
        this.dialog = false
        this.answer = ''
        this.snackbar = true
        this.text = '피드백 감사합니다'        
      }
    },
    register() {
      let sendData = {
        img_base64: this.encodedUrl,
        result: this.animal.english_name
      }
      let config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.post(SERVER.URL + SERVER.ROUTES.save, sendData, config)
      .then(res => {
        if (res.data.message === '저장 완료'){
          this.registered = true
          this.snackbar = true
          this.text = '도감에 등록되었습니다.'
        } else {
          this.snackbar = true
          this.text = '다시 한 번 시도해주세요'
        }
      })
    }
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn

    }
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
  font-size: 1.5rem;
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
.result-page {
  height: 100vh;
  width: 100vw;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 4;
}
.result-carousel {
  padding-bottom: 10vh;
}
.v-icon {
  color: grey !important;
}
.text-guide {
  color: #8A0000;
}
.btn-choice {
  font-size: 1rem;
}
.snackbar-content {
  font-size: large;
}
.adjust-text {
  font-size: large;
}
</style>