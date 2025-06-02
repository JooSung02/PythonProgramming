# 멀티모달 감정 인식 시스템

실시간 얼굴 감정 인식 웹 애플리케이션입니다. 웹캠을 통해 사용자의 얼굴을 감지하고 7가지 감정을 실시간으로 분석합니다.

## 주요 기능

- 실시간 얼굴 감지 및 추적
- 7가지 감정 상태 인식 (화남, 역겨움, 두려움, 행복, 슬픔, 놀람, 무표정)
- 얼굴 특징점(랜드마크) 감지
- 각 감정의 확률 실시간 표시
- 직관적인 웹 인터페이스

## 설치 가이드

1. 저장소 다운로드:
```bash
git clone https://github.com/JooSung02/PythonProgramming.git
cd Multimodal-Emotion-Recognition
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 모델 파일 준비:
- `Video/Models/EmotionXCeption/video.h5` 파일 다운로드
- `Video/Models/Landmarks/face_landmarks.dat` 파일 다운로드

## 실행 방법

1. 웹 서버 실행:
```bash
cd WebApp
python main.py
```

2. 웹 브라우저 접속:
- http://localhost:5000 주소로 접속

## 프로젝트 구성

```
Multimodal-Emotion-Recognition/
├── Video/                    # 비디오 감정 인식 모듈
│   ├── Models/              # 학습된 모델 파일들
│   └── Python/              # 파이썬 구현 코드
├── WebApp/                   # 웹 애플리케이션
│   ├── library/             # 핵심 라이브러리
│   ├── static/              # 정적 파일 (CSS, JS)
│   │   ├── js/             # 자바스크립트 파일
│   │   │   └── db/        # 데이터베이스 관련 파일
│   │   └── CSS/           # 스타일시트 파일
│   ├── templates/           # HTML 템플릿
│   └── main.py             # 웹 서버 메인 파일
└── requirements.txt         # 필요한 파이썬 패키지 목록
```

## 사용 기술

- Python: 주요 프로그래밍 언어
- OpenCV: 영상 처리 및 얼굴 감지
- dlib: 얼굴 랜드마크 감지
- TensorFlow/Keras: 딥러닝 모델
- Flask: 웹 서버 프레임워크
- HTML/CSS/JavaScript: 웹 인터페이스

## 라이선스

이 프로젝트는 MIT 라이선스로 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 프로젝트 기여

1. 이 저장소를 포크합니다.
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/새로운기능`).
3. 변경사항을 커밋합니다 (`git commit -m '새로운 기능 추가'`).
4. 브랜치를 푸시합니다 (`git push origin feature/새로운기능`).
5. Pull Request를 생성합니다.

## 문의 및 피드백

프로젝트에 대한 문의사항이나 개선 제안이 있으시면 이슈를 생성해주세요.
