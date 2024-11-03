from flask import Blueprint, request, jsonify, render_template
from flask_socketio import emit
import hashlib
import redis
from .llama import run_llama

summarize = Blueprint('summarize', __name__, template_folder='../templates')
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def init_socket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        print("[SOCKET] Client connected")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("[SOCKET] Client disconnected")

@summarize.route('/summarize', methods=['POST'])
def summarize_text():
    print("[ROUTE] Received summarize request")
    if request.method == 'OPTIONS':
        return "", 200

    try:
        data = request.get_json()
        print(f"[ROUTE] Received data: {data}")
        text_to_summarize = data.get('text', '')
        word_limit = data.get('word_limit', 50)
        print(f"[ROUTE] Text length: {len(text_to_summarize)}, Word limit: {word_limit}")

        summary = run_llama(text_to_summarize, word_limit)
        print("[ROUTE] Summary generated successfully")
        return jsonify({'summary': summary})

    except Exception as e:
        print(f"[ROUTE] Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@summarize.route('/')
def index():
    print("[ROUTE] Serving index page")
    return render_template('index.html')
