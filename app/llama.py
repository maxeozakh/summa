import subprocess

PATH_TO_LLAMA = './llama.cpp/'
MODEL_NAME = 'gemma-1.1-7b-it.Q4_K_M.gguf'
SUMMARY_LENGTH = 500


def run_llama(prompt, summa_len=SUMMARY_LENGTH):
    command = [
        f'{PATH_TO_LLAMA}llama-cli',
        '-m', f'{PATH_TO_LLAMA}models/{MODEL_NAME}',
        '--chat-template', 'gemma',
        '--no-warmup',
        '--no-display-prompt',
        '-i',
        '--prompt', f'Summarize the following text in {
            summa_len} words: {prompt}'
        # '-r', "User:",
        # '--in-prefix', "",
        # '--in-suffix', ">>>>>>>>",
    ]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, universal_newlines=True)

    for line in process.stdout:
        words = line.strip()
        print('NEW LINE', words)
