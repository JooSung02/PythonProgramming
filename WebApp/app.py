import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': '파일이 없습니다'})
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'success': False, 'error': '선택된 파일이 없습니다'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'filename': filename})
    
    return jsonify({'success': False, 'error': '허용되지 않는 파일 형식입니다'})

@app.route('/video_feed')
def video_feed():
    video_path = request.args.get('video_path')
    if video_path:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_path))
        if os.path.exists(video_path):
            return Response(generate_frames(video_path),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
    
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames(video_path=None):
    if video_path:
        cap = cv2.VideoCapture(video_path)
    else:
        cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # 감정 분석 수행
        results = analyze_emotions(frame)
        
        # 결과 시각화
        if results:
            for face in results:
                x, y, w, h = face['bbox']
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # 감정 레이블 표시
                emotion = max(face['emotions'].items(), key=lambda x: x[1])[0]
                cv2.putText(frame, emotion, (x, y-10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release() 