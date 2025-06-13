### General imports ###
import numpy as np
import cv2
from scipy.ndimage import zoom
import dlib
from imutils import face_utils
import os
import json

### Model ###
from tensorflow.keras.models import load_model

# 감정 레이블 정의
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# 콜백 저장용 변수
emotion_result_callback = None

def set_emotion_result_callback(cb):
    global emotion_result_callback
    emotion_result_callback = cb

def get_emotion_predictions(prediction):
    """
    예측 결과를 감정별 확률로 변환
    """
    emotions = {}
    for i, emotion in enumerate(EMOTIONS):
        emotions[emotion] = float(prediction[0][i])
    return emotions

def gen(video_path=None):
    """
    비디오 스트리밍 생성 함수
    video_path: 영상 파일 경로 (None이면 웹캠 사용)
    """
    print("비디오 스트리밍 시작...")
    
    # 비디오 소스 설정
    if video_path:
        print(f"영상 파일 로드: {video_path}")
        video_capture = cv2.VideoCapture(video_path)
    else:
        print("웹캠 활성화")
        video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("비디오 소스를 활성화할 수 없습니다.")
        return
    
    print("비디오 소스가 정상적으로 활성화되었습니다.")
    
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
                if video_path:
                    print("영상 파일의 끝에 도달했습니다.")
                    break
                else:
                    print("프레임을 읽을 수 없습니다.")
                    break
            
            # 그레이스케일 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 얼굴 감지
            rects = face_detect(gray, 1)
            
            # 감정 분석 결과 저장
            emotion_results = {}
            
            for (i, rect) in enumerate(rects):
                # 얼굴 좌표 가져오기
                (x, y, w, h) = face_utils.rect_to_bb(rect)
                face = gray[y:y+h, x:x+w]
                
                # 얼굴 이미지 크기 조정
                face = zoom(face, (48 / face.shape[0], 48 / face.shape[1]))
                face = face.astype(np.float32)
                face /= float(face.max())
                face = np.reshape(face.flatten(), (1, 48, 48, 1))
                
                # 감정 예측
                prediction = model.predict(face)
                emotion_results[f"face_{i+1}"] = get_emotion_predictions(prediction)
                
                # 얼굴 주변에 사각형 그리기
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # 감정 레이블 표시
                emotion_idx = np.argmax(prediction)
                emotion_label = EMOTIONS[emotion_idx]
                cv2.putText(frame, emotion_label, (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            
            # 결과를 JSON으로 인코딩
            emotion_json = json.dumps(emotion_results)
            
            # 콜백이 등록되어 있으면 호출
            if emotion_result_callback is not None:
                try:
                    emotion_result_callback(emotion_results)
                except Exception as cb_err:
                    print(f"emotion_result_callback error: {cb_err}")
            
            # 이미지를 JPEG로 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # 프레임과 감정 분석 결과를 함께 전송
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                   b'Content-Type: application/json\r\n\r\n' + emotion_json.encode() + b'\r\n')
                
        except Exception as e:
            print(f"프레임 처리 중 오류 발생: {str(e)}")
            break
    
    print("비디오 스트리밍 종료")
    video_capture.release()
