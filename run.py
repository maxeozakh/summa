from app import create_app

app, socketio = create_app()

application = app

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
