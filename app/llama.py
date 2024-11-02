import subprocess

path_to_llama = './llama.cpp/'
model_name = 'gemma-1.1-7b-it.Q4_K_M.gguf'
summary_length = 26

def run_llama(prompt, summa_len=summary_length):
    command = [
        f'{path_to_llama}llama-cli',
        '-m', f'{path_to_llama}models/{model_name}',
        '--chat-template', 'gemma',
        '--no-display-prompt',
        '-r', "User:",
        '--in-prefix', "",
        '--in-suffix', ">>>>>>>>",
        '--no-warmup',
        '--prompt', f'Summarize the following text in {summa_len} words: {prompt}'
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout