from flask import Flask, request,render_template
import os
from thehiveApi import create_case, create_observable, calculate_hash

# Flask 애플리케이션 생성
app = Flask(__name__)

# 전역 변수로 케이스 카운터 초기화
case_counter = 1

# 업로드된 파일을 저장할 디렉토리 경로
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 파일 업로드를 위한 폼
@app.route('/')
def upload_form():
    return render_template('index.html')

# 파일 업로드 처리 및 API 테스트
@app.route('/upload', methods=['POST'])
def upload_file():
    global case_counter  # <- 추가

    if 'file' not in request.files:
        return "파일이 선택되지 않았습니다."

    file = request.files['file']

    if file.filename == '':
        return "파일 이름이 비어 있습니다."

    # 업로드 폴더가 없으면 생성
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)


    case_title = f"Case {case_counter} "
    case_id = create_case(case_title, file.filename)
    if not case_id:
        return "케이스 생성 실패"

    case_counter += 1  # 카운터 증가

    # 해시 계산 및 Observable 생성
    hash_val = calculate_hash(file_path)
    observable_result = create_observable(case_id, hash_val)
    

    return f"파일이 업로드되었습니다: {file.filename}<br>Observable 결과: {observable_result}"

if __name__ == '__main__':
    app.run(debug=True)
