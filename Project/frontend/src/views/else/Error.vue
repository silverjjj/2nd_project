<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="error-subtitle py-0 font-weight-bold">존재하지 않는</v-col>
          <v-col cols="12" class="error-subtitle py-0 font-weight-bold">페이지 입니다</v-col>
          <v-col cols="12" class="error-detail pt-3">
            주소가 정확한지 확인 한 뒤 <br>
            잠시 후에 다시 시도해주세요
          </v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="text-size">
            <router-link to="/guide" class="text-decoration-none grey--text"><v-icon small class="mr-1">mdi-home</v-icon> 메인 화면으로 돌아가기</router-link>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
export default {
  name: 'error-page'
}
</script>

<style scoped>
.error-title {
  color: #8A0000;
  font-size: 3rem;
}
.error-subtitle {
  color: #8A0000;
  font-size: 1.5rem;
}
.error-detail {
  color: #8A0000;
  font-size: 1rem;
}
.error-guide {
  font-size: x-large;
}
.button-word {
  font-size: large;
  width: 70%
}
.text-size {
  font-size: 1rem;
}
</style>