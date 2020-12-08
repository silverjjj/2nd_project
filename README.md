# 특화 프로젝트 - 수상한 동물 사전(AI)

 ## 🐱‍💻 5252

| 이름          | 담당           |
| ------------- | -------------- |
| 김영수 (팀장) | AI + 풀 스택   |
| 구동엽        | 서버 + 백 엔드 |
| 이경민        | 백 엔드        |
| 이은재        | AI 개발        |
| 임혜민        | 프론트 엔드    |



## 1. 수상한 동물 사전 프로젝트란?   ![badge](https://img.shields.io/badge/%ED%8A%B9%ED%99%94PJT-5252-brightgreen)

**수상한 동물 사전** 프로젝트는 스캔 AI기술을 이용한 나만의 동물 도감 & 동물 분석입니다. 

'일상생활에서 만나는 동물의 종류가 궁금하신 분', '자신과 비슷한 동물을 궁금해 하시는 분'을 위해 **AI 동물 분석 도감**을 만들었습니다.

**「누구나 쉽고 간편하게 동물을 식별할 수 있고, 재밌게 자신과 닮은 동물을 만들 수 있는 모바일 웹」**을 목표로 합니다.

현재 총 100종의 동물이 있고 더욱 늘릴 예정입니다.

### 특징

- 언제 어디서나 동물, 인물 사진만 있으면 100종의 동물 중 같거나 비슷한 AI가 순식간에 검색해줍니다.

- 내가 닮은 동물 무엇인지 확인해 볼 수 있습니다.

- 여러분의 사진과 충분한 해설로 동물의 정보를 제공합니다.

- 커스터마이즈를 통해 하나 뿐인 나만의 동물 도감을 만들 수 있습니다.

  

<img src="https://blog.kakaocdn.net/dn/bOjw03/btqPql2eIg0/zGEMSEHIXne1N5FPr98eWk/img.png" alt="img" style="zoom:50%;" />



## 2. 수상한 동물 사전 프로젝트 정보

> 프로젝트를 시작하며 사용하게 되는 기술 스택 및 팀 룰에 관한 내용입니다.

### 2-1. 기술 스택 ![badge](https://img.shields.io/badge/%ED%8A%B9%ED%99%94PJT-5252-brightgreen)

-------------------------

![badge](https://img.shields.io/badge/browser-chrome-red)![badge](https://img.shields.io/badge/framework-Django%20Vue.js-yellow)![badge](https://img.shields.io/badge/DB-sqlite3-skyblue)![badge](https://img.shields.io/badge/node-12.18.2-brightgreen)![badge](https://img.shields.io/badge/npm-6.14.5-brightgreen)![badge](https://img.shields.io/badge/Vue.js-2.6.11-green)![badge](https://img.shields.io/badge/@vue/cli-4.4.6-green)![badge](https://img.shields.io/badge/yarn-1.22.4-blue)![badge](https://img.shields.io/badge/Django-2.1.15-orange)![badge](https://img.shields.io/badge/Python-3.7.6-orange)



| 구분        | 프레임워크         | 기타                        |
| ----------- | ------------------ | --------------------------- |
| 백엔드      | Django             | Django rest framework, SMTP |
| 프론트 엔드 | Vue.js             | Vuetify, nodeJS             |
| AI          | tensorflow         | Inception V3, Autocrawler   |
| DB          | sqlite3            |                             |
| Server      | Docker, AWS, Nginx |                             |



### 2-2. Git Convention

---

#### 2-2-1. Git-Branch

Git-flow는 다음과 같이 정해져있습니다.

- master : 배포 가능한 상태 브랜치
- develop : 업데이트 할 브랜치 + Docs 업데이트 브랜치
- feature : 기능을 개발하는 브랜치

#### 2-2-2. Git-commit

```bash
$ git commit -m "Jira 이슈 번호 | Header | 설명"
```

- JIRA 이슈 번호 or README
- Header
  - Initial : 가장 처음 만든 코드
  - Update : 정상적으로 동작하면서 수정/추가/보완된 코드
  - Fix : 비정상 동작 수정 코드

### 2-3. 와이어 프레임 & ERD

-----------------------------------

<img src="./Docs/wireframe.JPG">



### 2-4. 사용 패키지, 라이브러리

---

> `Project/frontend`의 `node_module`폴더와 `Project/backend`의 `requirements.txt` 참고.



## 3. 코드 리뷰

### 3-1 AI 모델

AI 모델은 Tensorflow를 활용한 CNN 신경망 구조 모델링을 개발했습니다. 한 클래스당 100장의 부족한 이미지 데이터를 보완하기 위해 data augmentation, 사전에 학습된 데이터셋인 VGG16과 Inception V3를 활용했습니다.

#### 데이터 수집 및 전처리

- 알파카, 뱅갈고양이, 닭 등 200장씩 100개 클래스의 이미지를 Auto crawling을 통해 데이터를 수집
- 200장의 사진 중 고화질 및 동물이 잘 나온 사진을 수작업으로 100장씩 선별
- 데이터 수 확보를 위해 data argumentation을 사용

```python
def add_input_distortions(flip_left_right, random_crop, random_scale,
                          random_brightness):
  jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput')
  decoded_image = tf.image.decode_jpeg(jpeg_data, channels=MODEL_INPUT_DEPTH)
  decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
  decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
  margin_scale = 1.0 + (random_crop / 100.0)
  resize_scale = 1.0 + (random_scale / 100.0)
  margin_scale_value = tf.constant(margin_scale)
  resize_scale_value = tf.random_uniform(tensor_shape.scalar(),
                                         minval=1.0,
                                         maxval=resize_scale)
  scale_value = tf.multiply(margin_scale_value, resize_scale_value)
  precrop_width = tf.multiply(scale_value, MODEL_INPUT_WIDTH)
  precrop_height = tf.multiply(scale_value, MODEL_INPUT_HEIGHT)
  precrop_shape = tf.stack([precrop_height, precrop_width])
  precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
  precropped_image = tf.image.resize_bilinear(decoded_image_4d,
                                              precrop_shape_as_int)
  precropped_image_3d = tf.squeeze(precropped_image, squeeze_dims=[0])
  cropped_image = tf.random_crop(precropped_image_3d,
                                 [MODEL_INPUT_HEIGHT, MODEL_INPUT_WIDTH,
                                  MODEL_INPUT_DEPTH])
  if flip_left_right:
    flipped_image = tf.image.random_flip_left_right(cropped_image)
  else:
    flipped_image = cropped_image
  brightness_min = 1.0 - (random_brightness / 100.0)
  brightness_max = 1.0 + (random_brightness / 100.0)
  brightness_value = tf.random_uniform(tensor_shape.scalar(),
                                       minval=brightness_min,
                                       maxval=brightness_max)
  brightened_image = tf.multiply(flipped_image, brightness_value)
  distort_result = tf.expand_dims(brightened_image, 0, name='DistortResult')
  return jpeg_data, distort_result
```



#### 모델 구현

- 이미지 데이터를 분석하는 CNN 신경망을 활용한 모델링 진행
- 일반화된 모델을 개발하기 위해 K-겹 교차검증 활용



#### 모델 검증 및 결과

- data augmentation, VGG16, InceptionV3을 각각 적용시킨 모델에 동일한 테스트 데이터셋으로 정확도 및 오차를 비교분석
- 높은 검증정확도와 과대적합이 발생하지 않은 InceptionV3를 활용한 모델 선정



### 3-2 Backend - Django

백엔드는 Tensorflow를 바로 사용하기 위해 Python 기반인 Django REST Framework를 기반으로 구현했습니다. Tensorflow를 이용해 예측하는 과정은 먼저 동기식으로 작성하였고, asyncio나 Django 최신버젼을 활용하고 thread를 활용하여 비동기 처리를 추가할 예정입니다. 개발 과정에서 이미지를 base64로 인코딩하여 사용했지만 Formdata를 활용하여 다시 사용하게 변경 예정입니다. 추가적으로 가지고 있는 동물 DB를 캐싱하여 좀더 빠르게 사용할 예정입니다.

개발 단계는 다음과 같습니다.

1. 작성한 와이어프레임과 ERD에 맞춘 Application 생성(계정을 관리할 Account, 이미지 예측 및 Tensorflow 사용할 Animal)

2. 카카오 정보를 활용한 회원가입 및 로그인 구현
   2-1. 카카오 회원 가입

    ```python
    @api_view(['POST'])
    def new_kakao(request):
        User = get_user_model()
        pwd = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        new_user = User.objects.create(username=request.data['username'], password=pwd, nickname=request.data['nickname'], email=request.data['email']) 
        new_user.register_login_method = User.REGISTER_LOGIN_KAKAO
        login(request, new_user, backend="django.contrib.auth.backends.ModelBackend")
        serializer = UserSerializer(new_user)
        return Response({'message':'신규 카카오 회원 로그인', "token": AuthToken.objects.create(new_user)[1], 'user': serializer.data})
    ```

    2-2. 카카오 로그인

    ```python
    @api_view(['POST'])
    def social_signup(request):
        nickname = request.data['nickname']
        if User.objects.filter(nickname=nickname).exists(): # DB에 존재하는 경우 로그인
            user = get_object_or_404(nickname=nickname)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return Response({'message':'기존 카카오 회원 로그인', 'token': AuthToken.objects.create(user)[1]})
        else: # DB에 존재하지 않는 경우 에러 반환
            return Response({'new': {'nickname': nickname, 'email':request.data['email']}})
        return Response({'message' : 'Error'})
    ```

3. Base64를 이용한 이미지 업로드, 예측 및 결과 저장 구현

4. (예정) 파일을 Formdata를 사용하여 전송

5. (예정) 비동기 이미지 예측 구현

6. (예정) 100마리 동물 정보를 캐싱



### 3-3 Frontend - Vue.js

프론트엔드는 Vue.js를 기반으로 구현했으며, vuex를 통해 상태를 관리하고 Vuetify를 통해 UI/UX를 고도화 하였습니다. 개발 작업은 **feature-기능명또는관련단어** 로 별도의 브랜치를 생성해 작업한 뒤 develop 브랜치로 머지하는 방식으로 진행해 코드 컨플릭트를 최소화하였습니다.

개발 단계는 다음과 같습니다.

1. 와이어프레임(화면 기획) 작성 
2. 라우터 처리 및 컴포넌트 구조화
3. Ajax 비동기 요청(axios)으로 백과 데이터 교환
4. vuex, vue-cookies를 활용한 state 관리
5. CSS 스타일링 및 UI/UX 고도화

특히, 수상한 동물사전의 핵심 기능이라고 볼 수 있는 AI 이미지 분석 기능의 경우 먼저 유저로부터 이미지를 입력받아 프론트에서 base64 인코딩을 진행한 뒤 백으로 인코딩된 값을 넘겨 AI 분석 함수를 실행시키는 로직으로 이루어져있습니다. 향후 프로젝트를 고도화할 경우, 인코딩 없이 firebase 또는 S3를 활용해 이미지를 서버에 업로드하여 해당 과정을 보다 간결하게 개선할 예정입니다.

다음은 프론트에서 이미지를 인코딩하는 데 활용한 주요 함수와 단계입니다. 

1 단계. 유저의 이미지 업로드 및 미리보기 구현을 위한 url생성

```jsx
onClickImageUpload() {
  this.selected = true
	// ref 속성이 imageInput인 input 태그를 클릭
  this.$refs.imageInput.click()
},
onChangeImages(e) {
	// 유저가 이미지를 업로드한 경우 실행되는 함수
	const file = e.target.files[0]
	this.imageUrl = URL.createObjectURL(file) // 미리보기로 이미지를 보여주기 위해 url생성
	this.createBase64Image(file) // base64인코딩을 시키기 위한 함수
},
```

2 단계. base64인코딩 작업

```jsx
createBase64Image(fileObject) {
  const reader = new FileReader()
  reader.onload = (e) => {
    var tempUrl = e.target.result
		// back에서 원하는 방식으로 데이터를 보내기 위한 작업
    this.adjustEncodedUrl(tempUrl) 
  }
  reader.readAsDataURL(fileObject)
},
adjustEncodedUrl(dataURL) {
  var strArray=dataURL.split(',')
  this.encodedUrl = strArray[1]
},
```

3 단계. 백으로 데이터를 넘긴 후 결과를 받아와 처리하는 작업

```jsx
nowclicked() {
	// v-if 로 로딩처리를 하기 위한 flag
  this.searched = true
  this.isloading = true

	// back으로 보내는 객체 생성
  const analysisData = {
    img_base64: this.encodedUrl
  }

  axios.post(SERVER.URL + SERVER.ROUTES.predict, analysisData)
    .then(res => {
      this.isloading = false
      var ele = []
      res.data.result.forEach(function(element) {
				// 유사 리스트 관련 처리
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
```



###  주요 화면

![img](https://blog.kakaocdn.net/dn/6vNmz/btqPqlVlIrn/Q4q2lAPashMzY5nmP38OH0/img.png)

 [화면 더 보기....pdf](Docs\화면 더 보기....pdf) 



### 소개 UCC 

[클릭](https://www.youtube.com/watch?v=z_UUmDXXtuk)해주세요.



### 참고자료

 [최종 발표자료.pdf](Docs\최종 발표자료.pdf) 