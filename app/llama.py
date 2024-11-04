import subprocess
import signal
import os
import time
from flask import current_app

PATH_TO_LLAMA = './llama.cpp/'
MODEL_NAME = 'gemma-1.1-7b-it.Q4_K_M.gguf'
SUMMARY_LENGTH = 500


def run_llama(prompt, summa_len=SUMMARY_LENGTH):
    print("[LLAMA] Starting llama process")
    print(f"[LLAMA] Prompt length: {len(prompt)}")

    command = [
        f'{PATH_TO_LLAMA}llama-cli',
        '-m', f'{PATH_TO_LLAMA}models/{MODEL_NAME}',
        '--chat-template', 'gemma',
        '--no-warmup',
        '--no-display-prompt',
        '-i',
        '--prompt', f'Summarize the following text in {
            summa_len} words: {prompt}'
    ]
    print(f"[LLAMA] Command: {' '.join(command)}")

    full_response = []
    process = None
    start_time = time.time()

    try:
        print("[LLAMA] Creating subprocess")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        socketio = current_app.extensions['socketio']
        print("[LLAMA] Got socketio instance")

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            words = line.strip()
            if words:
                print(f"[LLAMA] Generated text: {words[:50]}...")
                full_response.append(words)
                socketio.emit('llama_output', {'data': words})

        elapsed_time = time.time() - start_time
        print(f"[LLAMA] Process completed in {elapsed_time:.2f} seconds")

        # Remove callback and just emit the event
        socketio.emit('llama_complete', {
            'elapsed_time': elapsed_time,
            'total_tokens': len(full_response)
        })

        # Add debug print after emission
        print("[LLAMA] Completion event emitted")

        result = ' '.join(full_response)
        return result

    except Exception as e:
        print(f"[LLAMA] Error occurred: {str(e)}")
        raise
    finally:
        if process:
            print("[LLAMA] Starting cleanup...")
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                print("[LLAMA] Process group terminated")
            except Exception as e:
                print(f"[LLAMA] Error in cleanup: {str(e)}")
            process.terminate()
            process.wait(timeout=1)
