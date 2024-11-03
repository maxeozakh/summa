from flask import Blueprint, request, jsonify, render_template
import redis
import hashlib
from .llama import run_llama  # Ensure this is properly set up

summarize = Blueprint('summarize', __name__, template_folder='../templates')

redis_client = redis.Redis(host='localhost', port=6379, db=0)


@summarize.route('/')
def home():
    return render_template('index.html')


def get_cache_key(prompt, word_limit):
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    return f"summary:{prompt_hash}:{word_limit}"


@summarize.route('/summarize', methods=['POST'])
def summarize_text():
    if request.method == 'OPTIONS':
        print("OPTIONS request received")
        return "", 200

    try:
        data = request.get_json()
        text_to_summarize = data.get('text', '')
        word_limit = data.get('word_limit', 50)

        global summary_length
        summary_length = word_limit

        # Check cache
        cache_key = get_cache_key(text_to_summarize, word_limit)
        cached_summary = redis_client.get(cache_key)
        if cached_summary:
            print('Returning cached summary')
            return jsonify({'summary': cached_summary.decode()})

        # Run summarization if not cached
        summary = run_llama(text_to_summarize, word_limit)

        # Store result in cache
        redis_client.set(cache_key, summary)

        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
