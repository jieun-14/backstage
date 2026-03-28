from flask import Flask, jsonify, request
import datetime
import socket

app = Flask(__name__)


@app.route('/api/v1/details1')
def details1():
    return '<h1>Hello World!</h1>'

@app.route('/api/v1/details2')
def details2():
    return jsonify({
        'message': 'Hello World!',
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'hostname': socket.gethostname(),
        'ip': request.remote_addr,
        'message2': '이지은짱!!',
        'message3': '추카추카추!!!',
        'message4': 'self hosted runner!!!'
    })


@app.route('/api/v1/healthz')
def healthz():
    return jsonify({
        'status': 'UP'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# '/api/v1/details' http://127.0.0.1:5000/api/v1/details 접속!!!
# '/api/v1/healthz'

