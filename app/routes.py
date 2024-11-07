import uuid
from flask import Blueprint, request, jsonify, render_template, make_response
from app.llama import run_llama
from app.queue import add_to_queue
from app.session import user_connections

summarize = Blueprint('summarize', __name__, template_folder='../templates')


def init_socket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        user_id = request.cookies.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            print(
                '[ROUTE] User ID was not founded in cookies, so we generate it on socket connection instead %) %)')

        user_connections[user_id] = request.sid
        socketio.emit('user_id', {'user_id': user_id})
        print(f"[SOCKET] Client connected with user_id {user_id}")

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = None
        # Find user_id by socket id
        for uid, sid in user_connections.items():
            if sid == request.sid:
                user_id = uid
                break

        if user_id:
            user_connections.pop(user_id, None)
        print(f"[SOCKET] Client disconnected, removed user_id {user_id}")


@summarize.route('/summarize', methods=['POST'])
def summarize_text():
    print("[ROUTE] Received summarize request")
    if request.method == 'OPTIONS':
        return "", 200

    try:
        user_id = request.cookies.get('user_id')
        if not user_id:
            print('[ROUTE] User ID not found in cookies')
            return jsonify({'error': 'User ID not found in cookies'}), 400

        data = request.get_json()
        text_to_summarize = data.get('text', '')
        word_limit = data.get('word_limit', 50)
        text_len = len(text_to_summarize)
        print(f"[ROUTE] Text length: {text_len}, Word limit: {word_limit}")

        def task(text, user_id, limit):
            summary = run_llama(text, user_id, limit)
            print("[ROUTE] Summary generated successfully", summary[:5], "...")

        add_to_queue(lambda: task(text_to_summarize, user_id, word_limit))
        return jsonify({'status': 'task added to the queue'})

    except Exception as e:
        print(f"[ROUTE] Error occurred: {str(e)}", e)
        return jsonify({'error': str(e)}), 500


@summarize.route('/')
def index():
    print("[ROUTE] Serving index page")
    user_id = str(uuid.uuid4())
    response = make_response(render_template('index.html'))
    response.set_cookie('user_id', user_id, path='/', samesite='Lax')
    user_connections[user_id] = None  # This updates when socket connects
    return response
