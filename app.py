from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    # 0.0.0.0로 서버 실행하여 외부 접속 허용
    app.run(debug=True, host='0.0.0.0', port=5000)
