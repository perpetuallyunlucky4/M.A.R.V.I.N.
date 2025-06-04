from llama_cpp import Llama
import time
import os, sys
import json
import re
import subprocess
from pluginManager import pluginManager
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

time_update_interval = 5
message_counter = 0

pm = pluginManager()
pm.load_plugins()
print(pm.plugins)

#model_path="/home/pi/llama.cpp/models/codellama-7b-instruct.Q4_K_M.gguf"
model_path = "/home/pi/Downloads/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"

gen_code_path = "marvin_code.py"

max_history = 10

llm = Llama(model_path,
            n_threads=4,
            chat_format="chatml",
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
        user_input = input("\033[38;2;0;255;255mniko: \033[0m")
        chat_history.append({
            "role" : "user",
            "content" : user_input,
        })
        
        message_counter += 1
        
        if len(chat_history) > 2 * max_history + 1:
            chat_history = [chat_history[0]] + chat_history[-(2 * max_history):]
            
        if message_counter >= time_update_interval:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\033[38;2;255;60;60m\nThe current time is {current_time}\033[0m")
            chat_history.append({
                    "role" : "system",
                    "content" : f"The current time is {current_time}"
                })
            message_counter = 0

        
        print("\033[38;2;255;20;147mmarvin: \033[0m", end="", flush=True)
        
        stream = llm.create_chat_completion(messages=chat_history,
                                            stream=True,
                                            max_tokens=1000,
                                            temperature=0.3,
                                            top_p=0.7,
                                            top_k=40
                                        )
        
        marvin_reply = ""
        for chunk in stream:
            token = chunk["choices"][0]["delta"].get("content", "")
            print(f"\033[38;2;255;182;193m{token}\033[0m", end="", flush=True)
            marvin_reply += token
            
        print()
      
        chat_history.append({
            "role" : "assistant",
            "content" : marvin_reply.strip()
        })
        
        plugin_responses = pm.run_plugins(marvin_reply)
        if plugin_responses != []:
            for response in plugin_responses:
                print(f"\033[38;2;255;60;60msystem: {response}\n\033[0m")
                chat_history.append({
                    "role" : "system",
                    "content" : response.strip()
                })
                chat_history.append({
                    "role" : "user",
                    "content" : f"marvin, the plugin returned this:{response.strip()}\n. Please summarize it within a few sentences, taking into account what the user previously asked."
                })
                
                print("\033[38;2;255;20;147mmarvin: \033[0m", end="", flush=True)
        
                stream = llm.create_chat_completion(messages=chat_history,
                                                    stream=True,
                                                    max_tokens=1000,
                                                    temperature=0.3,
                                                    top_p=0.7,
                                                    top_k=40
                                                )
        
                marvin_reply = ""
                for chunk in stream:
                    token = chunk["choices"][0]["delta"].get("content", "")
                    print(f"\033[38;2;255;182;193m{token}\033[0m", end="", flush=True)
                    marvin_reply += token
            
                print()
      
                chat_history.append({
                    "role" : "assistant",
                    "content" : marvin_reply.strip()
                })
        
        with open(history_path, "w") as file:
            json.dump(chat_history, file, indent=2)
        
except KeyboardInterrupt:
    print("\033[38;2;255;60;60m\nmarvin: goodbye, Sir\033[0m")
    print("\033[38;2;255;60;60m\nsystem shutting down...\033[0m")

        
        
        
        
