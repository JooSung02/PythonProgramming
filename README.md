<<<<<<< HEAD
# 멀티모달 감정 인식 시스템

실시간으로 얼굴 표정을 분석하여 감정을 인식하는 웹 애플리케이션입니다.

## 주요 기능

- 실시간 웹캠을 통한 감정 분석
- 영상 파일 업로드 및 감정 분석
- 7가지 감정 분류 (행복, 슬픔, 분노, 놀람, 중립, 혐오, 두려움)
- 실시간 감정 분석 결과 시각화

## 기술 스택

- Python 3.8+
- Flask
- TensorFlow
- OpenCV
- dlib
- HTML/CSS/JavaScript

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/[your-username]/Multimodal-Emotion-Recognition.git
cd Multimodal-Emotion-Recognition
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 모델 파일 다운로드
- `Models` 폴더에 다음 파일들이 필요합니다:
  - `video.h5`: 감정 인식 모델
  - `face_landmarks.dat`: 얼굴 랜드마크 모델

## 실행 방법

1. 서버 실행
```bash
python WebApp/main.py
```

2. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 사용 방법

1. 웹캠을 통한 실시간 감정 분석
   - 웹캠이 연결된 상태에서 페이지 접속
   - 자동으로 감정 분석 시작

2. 영상 파일을 통한 감정 분석
   - "영상 선택" 버튼 클릭
   - 지원되는 형식: MP4, AVI, MOV, MKV
   - "업로드" 버튼 클릭
   - 자동으로 영상 재생 및 감정 분석 시작

## 프로젝트 구조

```
Multimodal-Emotion-Recognition/
├── WebApp/
│   ├── main.py
│   ├── app.py
│   ├── library/
│   │   └── video_emotion_recognition.py
│   ├── templates/
│   │   ├── index.html
│   │   └── video.html
│   └── Models/
│       ├── video.h5
│       └── face_landmarks.dat
├── requirements.txt
└── README.md
```

## 라이선스

MIT License

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 문의 및 피드백

프로젝트에 대한 문의사항이나 개선 제안이 있으시면 이슈를 생성해주세요.
=======
팀장: 박주성
<br/>
팀원: 윤세연
>>>>>>> 6a02740e69b467ac55df4b0f9d9da984593edaab
