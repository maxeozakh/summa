import subprocess
import time
from flask import current_app
from app.session import user_connections

PATH_TO_LLAMA = './llama.cpp/'
MODEL_NAME = 'gemma-1.1-7b-it.Q4_K_M.gguf'
SUMMARY_LENGTH = 500


def run_llama(prompt, user_id, summa_len=SUMMARY_LENGTH):
    print("[LLAMA] Starting llama process")
    print(f"[LLAMA] Prompt length: {len(prompt)}")

    command = [
        f'{PATH_TO_LLAMA}llama-cli',
        '-m', f'{PATH_TO_LLAMA}models/{MODEL_NAME}',
        '--chat-template', 'openchat',
        # '--chat-template', 'orion',
        # '--chat-template', 'gemma',
        '--temp', '0.5',
        '--no-warmup',
        '--no-display-prompt',
        '--prompt', f'Summarize the following text in {
            summa_len} words: {prompt}'
    ]

    full_response = []
    process = None
    start_time = time.time()

    try:
        print("[LLAMA] Creating subprocess")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=False,
        )

        socketio = current_app.extensions['socketio']
        print("[LLAMA] Got socketio instance")

        socketio.emit('llama_started', room=user_connections[user_id])
        while True:
            byte = process.stdout.read(1)  # Read one byte at a time
            if byte == b'':  # End of output
                break
            try:
                # Decode the byte to a string
                # utf-8 decoding, handle any errors as needed
                character = byte.decode('utf-8')
                full_response.append(character)
                socketio.emit('llama_output', {
                              'data': character}, room=user_connections[user_id])
            except UnicodeDecodeError:
                # Handle any decoding errors here, if necessary
                print("[LLAMA] Skipping invalid byte in output")

        elapsed_time = time.time() - start_time
        print(f"[LLAMA] Process completed in {elapsed_time:.2f} seconds")

        # Remove callback and just emit the event
        socketio.emit('llama_complete', {
            'elapsed_time': elapsed_time,
            'total_tokens': len(full_response)
        }, room=user_connections[user_id])

        print("[LLAMA] Completion event emitted")

        result = ' '.join(full_response)
        return result

    except Exception as e:
        print(f"[LLAMA] Error occurred: {str(e)}")
        raise
    finally:
        if process:
            print("[LLAMA] Starting cleanup...", process, process.pid)
            try:
                # Send SIGTERM to allow the subprocess to clean up
                process.terminate()
                process.wait(timeout=5)  # Wait for the process to exit
                print("[LLAMA] Subprocess terminated gracefully")
            except subprocess.TimeoutExpired:
                print("[LLAMA] Subprocess did not terminate in time, killing it")
                process.kill()
                process.wait()
            except Exception as e:
                print(f"[LLAMA] Error in cleanup: {str(e)}")
