import subprocess

PATH_TO_LLAMA = './llama.cpp/'
MODEL_NAME = 'gemma-1.1-7b-it.Q4_K_M.gguf'
SUMMARY_LENGTH = 26


def run_llama(prompt, summa_len=SUMMARY_LENGTH):
    command = [
        f'{PATH_TO_LLAMA}llama-cli',
        '-m', f'{PATH_TO_LLAMA}models/{MODEL_NAME}',
        '--chat-template', 'gemma',
        '--no-display-prompt',
        '-r', "User:",
        '--in-prefix', "",
        '--in-suffix', ">>>>>>>>",
        '--no-warmup',
        '--prompt', f'Summarize the following text in {
            summa_len} words: {prompt}'
    ]

    result = subprocess.run(
        command, stdout=subprocess.PIPE, text=True, check=True)
    return result.stdout
