<template>
  <div class="d-flex flex-column justify-center align-center">
    <div class="d-flex justify-center align-center text-center">
      <v-container>
        <v-row>
          <v-col cols="12" class="home-title py-0 mb-1 font-weight-bold">수상한</v-col>
          <v-col cols="12" class="home-title py-0 font-weight-bold">동물사전</v-col>
        </v-row>
        <v-row class="mt-5">
          <v-col cols="12" class="py-4">
            <router-link to="/mypage" class="text-decoration-none home-guide black--text">내 사전 보기</router-link>
          </v-col>
          <v-col cols="12" class="py-0">
            <router-link to="/guide" class="text-decoration-none home-guide black--text">사전 구경하기</router-link>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home'
}
</script>

<style scoped>
.home-title {
  color: #8A0000;
  font-size: 3rem;
}
.home-guide {
  font-size: x-large;
}
</style>