import uuid
from flask import Blueprint, request, jsonify, render_template, make_response, current_app
from app.llama import run_llama
from app.queue import add_to_queue, get_queued_and_active_tasks_amount, get_last_queued_task_index
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


def summary_done_callback(task_index):
    socketio = current_app.extensions['socketio']
    socketio.emit('done_task_index', {'task_index': task_index})
    print('[QUEUE]: task is DONE', '\n')


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

        def task(text, user_id, limit):
            summary = run_llama(text, user_id, limit)
            print("[ROUTE] Summary generated successfully", summary[:5], "...")

        # Get task index based on both queued and active tasks

        current_task_index = 1

        last_queued_task_index = get_last_queued_task_index()
        if (last_queued_task_index > 0):
            current_task_index = last_queued_task_index + 1

        add_to_queue(
            current_task_index,
            lambda: task(text_to_summarize, user_id, word_limit),
            lambda: summary_done_callback(current_task_index)
        )
        return jsonify({'status': 'task added to the queue', 'task_index': current_task_index})

    except Exception as e:
        print(f"[ROUTE] Error occurred: {str(e)}", e)
        return jsonify({'error': str(e)}), 500


@ summarize.route('/')
def index():
    print("[ROUTE] Serving index page")
    user_id = str(uuid.uuid4())
    response = make_response(render_template('index.html'))
    response.set_cookie('user_id', user_id, path='/', samesite='Lax')
    user_connections[user_id] = None  # This updates when socket connects
    return response
