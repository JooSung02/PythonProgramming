from flask import Flask, render_template, Response
import os

app = Flask(__name__)

try:
    from library.video_emotion_recognition import gen
    print("video_emotion_recognition 모듈 임포트 성공")
except Exception as e:
    print(f"video_emotion_recognition 모듈 임포트 실패: {e}")
    def gen():
        return "모듈 로드 실패"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("서버 시작...")
    app.run(debug=True)
