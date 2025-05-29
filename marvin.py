from llama_cpp import Llama
import time
import os
import json
import re
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

model_path="/home/pi/llama.cpp/models/codellama-7b-instruct.Q4_K_M.gguf"

gen_code_path = "marvin_code.py"

max_history = 10

llm = Llama(model_path,
            n_threads=4,
            chat_format="llama-2",
            verbose=False,
            n_ctx=2048
        )

history_path = "history.json"

if os.path.exists(history_path):
    with open(history_path, "r") as file:
        chat_history = json.load(file)
else:
    print("no chat history!")

try:
    while True:
        user_input = input(Fore.BLUE + "niko: " + Style.RESET_ALL)
        chat_history.append({
            "role" : "user",
            "content" : user_input,
        })
        
        if len(chat_history) > 2 * max_history + 1:
            chat_history = [chat_history[0]] + chat_history[-(2 * max_history):]

        
        print(Fore.GREEN + "marvin: " + Style.RESET_ALL, end="", flush=True)
        stream = llm.create_chat_completion(messages=chat_history,
                                            stream=True,
                                            max_tokens=300,
                                            temperature=0.3,
                                            top_p=0.7,
                                            top_k=40
                                        )
        
        marvin_reply = ""
        for chunk in stream:
            token = chunk["choices"][0]["delta"].get("content", "")
            print(Fore.CYAN + token, end="", flush=True)
            marvin_reply += token
            
        print()
      
        chat_history.append({
            "role" : "assistant",
            "content" : marvin_reply.strip()
        })
        
        with open(history_path, "w") as file:
            json.dump(chat_history, file, indent=2)
        
except KeyboardInterrupt:
    print(Style.BRIGHT + Fore.RED + "\nmarvin: goodbye, Sir" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.RED + "system shutting down..." + Style.RESET_ALL)

        
        
        
        
