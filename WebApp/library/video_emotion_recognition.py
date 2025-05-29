### General imports ###
import numpy as np
import cv2
from scipy.ndimage import zoom
import dlib
from imutils import face_utils
import os

### Model ###
from tensorflow.keras.models import load_model

def gen():
    """
    비디오 스트리밍 생성 함수
    """
    print("비디오 스트리밍 시작...")
    
    # 비디오 캡처 시작
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("웹캠을 활성화할 수 없습니다.")
        return
    
    print("웹캠이 정상적으로 활성화되었습니다.")
    
    # 현재 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    
    # 모델 파일 경로
    model_path = os.path.join(base_dir, 'Models', 'video.h5')
    print(f"모델 경로: {model_path}")
    
    if not os.path.exists(model_path):
        print(f"모델 파일이 존재하지 않습니다: {model_path}")
        return
    
    # 모델 로드
    model = load_model(model_path)
    print("모델 로딩이 완료되었습니다.")
    
    # 얼굴 감지기 로드
    face_detect = dlib.get_frontal_face_detector()
    print("얼굴 감지기가 로드되었습니다.")
    
    # 랜드마크 예측기 로드
    landmarks_path = os.path.join(base_dir, 'Models', 'face_landmarks.dat')
    print(f"랜드마크 파일 경로: {landmarks_path}")
    
    if not os.path.exists(landmarks_path):
        print(f"랜드마크 파일이 존재하지 않습니다: {landmarks_path}")
        return
    
    predictor_landmarks = dlib.shape_predictor(landmarks_path)
    print("랜드마크 예측기가 로드되었습니다.")
    
    # 랜드마크 인덱스 초기화
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    (jStart, jEnd) = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]
    (eblStart, eblEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
    (ebrStart, ebrEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
    
    # 임시 디렉토리 생성
    tmp_dir = os.path.join(base_dir, 'tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print(f"임시 디렉토리 생성됨: {tmp_dir}")
    
    while True:
        try:
            # 프레임 캡처
            ret, frame = video_capture.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break
            
            # 그레이스케일 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 얼굴 감지
            rects = face_detect(gray, 1)
            
            # 감지된 얼굴에 대해 처리
            for (i, rect) in enumerate(rects):
                # 얼굴 좌표 가져오기
                (x, y, w, h) = face_utils.rect_to_bb(rect)
                face = gray[y:y+h, x:x+w]
                
                # 랜드마크 감지
                shape = predictor_landmarks(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                # 얼굴 크기 조정
                face = cv2.resize(face, (48, 48))
                face = face.astype(np.float32)
                face /= 255.0
                face = np.reshape(face, (1, 48, 48, 1))
                
                # 감정 예측
                prediction = model.predict(face)
                prediction_result = np.argmax(prediction)
                
                # 감정 레이블과 확률 계산
                emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
                emotion = emotions[prediction_result]
                
                # 각 감정의 확률을 퍼센트로 계산
                probabilities = prediction[0] * 100
                
                # 좌측 상단에 각 감정의 확률 표시
                y_offset = 30
                for i, (emotion_name, prob) in enumerate(zip(emotions, probabilities)):
                    text = f"{emotion_name}: {prob:.1f}%"
                    cv2.putText(frame, text, (10, y_offset + i*30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # 얼굴 주변에 사각형 그리기
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # 현재 감정 레이블 추가
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # 랜드마크 그리기
                for (j, k) in shape:
                    cv2.circle(frame, (j, k), 1, (0, 0, 255), -1)
                
                # 눈 그리기
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                # 코 그리기
                nose = shape[nStart:nEnd]
                noseHull = cv2.convexHull(nose)
                cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)
                
                # 입 그리기
                mouth = shape[mStart:mEnd]
                mouthHull = cv2.convexHull(mouth)
                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
                
                # 턱 그리기
                jaw = shape[jStart:jEnd]
                jawHull = cv2.convexHull(jaw)
                cv2.drawContours(frame, [jawHull], -1, (0, 255, 0), 1)
                
                # 눈썹 그리기
                leftEyebrow = shape[eblStart:eblEnd]
                rightEyebrow = shape[ebrStart:ebrEnd]
                leftEyebrowHull = cv2.convexHull(leftEyebrow)
                rightEyebrowHull = cv2.convexHull(rightEyebrow)
                cv2.drawContours(frame, [leftEyebrowHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyebrowHull], -1, (0, 255, 0), 1)
            
            # 프레임 저장
            tmp_path = os.path.join(base_dir, 'tmp', 't.jpg')
            cv2.imwrite(tmp_path, frame)
            
            # 프레임 전송
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open(tmp_path, 'rb').read() + b'\r\n')
                
        except Exception as e:
            print(f"프레임 처리 중 오류 발생: {str(e)}")
            break
    
    print("비디오 스트리밍 종료")
    video_capture.release()
