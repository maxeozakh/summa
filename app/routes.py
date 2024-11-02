from flask import Blueprint, request, jsonify
from .llama import run_llama
import redis
import hashlib

summarize = Blueprint('summarize', __name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_cache_key(prompt, word_limit):
    # Generate a unique cache key based on input text and word limit
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    return f"summary:{prompt_hash}:{word_limit}"

@summarize.route('/summarize', methods=['POST', 'OPTIONS', 'GET'])
def summarize_text():
    # Handle preflight OPTIONS requests
    if request.method == 'OPTIONS':
        print("OPTIONS request received")
        return '', 200

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
        
        # Cache the result
        
        redis_client.set(cache_key, summary.strip(), ex=3600)  # Cache for 1 hour

        print('summary: ', summary)
        return jsonify({'summary': summary.strip()})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
