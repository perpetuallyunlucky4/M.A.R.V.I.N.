from llama_cpp import Llama
import os, sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#model_path="/home/pi/llama.cpp/models/codellama-7b-instruct.Q4_K_M.gguf"
model_path = "/home/pi/llama.cpp/models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"

max_history = 15

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

def generate_chat_completion(message):
    global chat_history
    chat_history.append({
        "role" : "user",
        "content" : message,
    })
                
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
        marvin_reply += token
        yield token

    chat_history.append({
        "role" : "assistant",
        "content" : marvin_reply.strip()
    })
        
    if len(chat_history) > (2 * max_history + 1):
        chat_history = [chat_history[0]] + chat_history[-(max_history * 2):]

    
    with open(history_path, "w") as file:
        json.dump(chat_history, file, indent=2)


def test_tokens(dummy):
    reply = "This is a test of the WEB UI's token streaming capabilities"
    for token in reply.split():
        time.sleep(0.5) 
        yield token

        

        
        
        


