from flask import Flask, render_template, Response, jsonify, request
import os
import threading
import time
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': '선택된 파일이 없습니다.'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'filename': filename})
    
    return jsonify({'error': '허용되지 않는 파일 형식입니다.'}), 400

@app.route('/video_feed')
def video_feed():
    video_path = request.args.get('video_path')
    if video_path:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_path)
        if not os.path.exists(video_path):
            return "영상 파일을 찾을 수 없습니다.", 404
    return Response(gen(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

# 실시간 감정 결과 반환 API
@app.route('/emotion_feed')
def emotion_feed():
    with lock:
        return jsonify(latest_emotion_result)

if __name__ == '__main__':
    print("서버 시작...")
    app.run(debug=True)
