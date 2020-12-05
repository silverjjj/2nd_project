<template>
  <div class="d-flex justify-center align-center">
    <v-container>
      <v-row>
        <v-col cols="12" class="py-0 text-center">No. <span class="font-weight-bold">{{selectedAnimalPK}}</span></v-col>
        <v-col cols="12" class="animal-name text-center pb-0">{{selectedAnimal.name}}</v-col>
        <v-col cols="12" class="animal-ename text-center pt-0">{{selectedAnimal.english_name}}</v-col>
        <v-col cols="12">
          <v-carousel
              height="300"
              hide-delimiters
              show-arrows>
              <v-carousel-item
                v-for="(imglink, index) in selectedAnimal.images"
                :key="index"
                light>
                  <v-card height="100%" class="d-flex flex-column justify-center align-center">
                    <div>
                      <img :src="'/api'+imglink" alt="" width="100%">
                    </div>
                    <div class="d-flex justify-center">
                      발견 일자 : {{selectedAnimal.upload_date[index].substr(0,10)}}
                    </div>
                  </v-card>
              </v-carousel-item>
            </v-carousel>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'FoundModal',
  props: [
    'selectedAnimal', 'selectedAnimalPK'
  ],
  data() {
    return {
      
    }
  }
}
</script>

<style scoped>
.animal-name {
  font-size: x-large;
  font-weight: bold;
}
.animal-ename {
  font-size: medium;
  color: grey;
}
</style>