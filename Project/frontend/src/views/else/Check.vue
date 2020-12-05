<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="check-subtitle py-0 font-weight-bold">회원 인증이 필요한</v-col>
          <v-col cols="12" class="check-subtitle py-0 font-weight-bold">서비스 입니다.</v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="py-1">
            <router-link to="/auth" class="text-decoration-none">
            <v-btn outlined color="#8A0000" class="button-word font-weight-bold"><v-icon small class="mr-2">mdi-account</v-icon> 로그인 하러가기</v-btn>
            </router-link>
          </v-col>
          <v-col cols="12" class="py-1">
            <router-link to="/guide" class="text-decoration-none">
            <v-btn outlined color="#8A0000" class="button-word font-weight-bold"><v-icon small class="mr-2">mdi-home</v-icon> 홈으로 돌아가기</v-btn>
            </router-link>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
export default {
  name: 'check'
}
</script>

<style scoped>
.check-title {
  color: #8A0000;
  font-size: 3rem;
}
.check-subtitle {
  color: #8A0000;
  font-size: 1.5rem;
}
.check-detail {
  color: #8A0000;
  font-size: 1rem;
}
.check-guide {
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