from flask import Flask, render_template
from flask_socketio import SocketIO
from utils.get_data import get_time
from utils.get_data import get_data


app = Flask(__name__)
socketio = SocketIO(app)

# 主页路由
@app.route('/')
def home():
    return render_template('home.html', days = get_time())

# 预测
@app.route('/pred')
def pred():
    return render_template('pred.html')

# 今日到单
@app.route('/today')
def today():
    # print(get_mysql())
    return render_template('today.html', data = get_data(), col = get_data().shape[0])

# 后台线程每5秒推送数据
def background_task():
    while True:
        socketio.sleep(5)
        data = get_data()
        data_dict = data.to_dict(orient='records')
        socketio.emit('update_data', {
            "data": data_dict,
            "col": data.shape[0]
        })
        # print(data_dict)
@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(background_task)

# 前端
@app.route('/previous')
def previous():
    return render_template('previous.html')

# 后端
@app.route('/back')
def back():
    return render_template('back.html')

if __name__ == '__main__':
    # app.run('0.0.0.0', port = 8888, debug = True)
    socketio.run(app, host='0.0.0.0', port=8888, debug=True, allow_unsafe_werkzeug = True)