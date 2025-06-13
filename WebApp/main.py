from flask import Flask, render_template, Response, jsonify
import os
import threading
import time
import json

app = Flask(__name__)

try:
    from library.video_emotion_recognition import gen, set_emotion_result_callback
    print("video_emotion_recognition 모듈 임포트 성공")
except Exception as e:
    print(f"video_emotion_recognition 모듈 임포트 실패: {e}")
    def gen():
        return "모듈 로드 실패"
    def set_emotion_result_callback(cb):
        pass

# 전역 변수로 감정 결과 저장
latest_emotion_result = {}
lock = threading.Lock()

def emotion_result_callback(result):
    global latest_emotion_result
    with lock:
        latest_emotion_result = result

# gen()에서 감정 결과가 나올 때마다 콜백으로 저장
set_emotion_result_callback(emotion_result_callback)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 실시간 감정 결과 반환 API
@app.route('/emotion_feed')
def emotion_feed():
    with lock:
        return jsonify(latest_emotion_result)

if __name__ == '__main__':
    print("서버 시작...")
    app.run(debug=True)
