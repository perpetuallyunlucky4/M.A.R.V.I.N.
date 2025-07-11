from llama_cpp import Llama
import os, sys
import json
import time
from plugin_manager import pluginManager

pm = pluginManager()
pm.load_plugins()
print(pm.plugins)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#model_path="/home/pi/llama.cpp/models/codellama-7b-instruct.Q4_K_M.gguf"
model_path = "/home/pi/llama.cpp/models/Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf"

max_history = 8

llm = Llama(model_path,
            n_threads=4,
            chat_format="chatml",
            verbose=False,
            n_ctx=4096
        )

history_path = "history.json"

if os.path.exists(history_path):
    with open(history_path, "r") as file:
        chat_history = json.load(file)
else:
    print("no chat history!")

def get_history():
    return chat_history

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

    yield "__END__"
    marvin_reply = ""
    for chunk in stream:
        token = chunk["choices"][0]["delta"].get("content", "")
        marvin_reply += token
        yield f"__APPEND__{token}"
    yield "__END__"
    
    chat_history.append({
        "role" : "assistant",
        "content" : marvin_reply.strip()
    })
        
    plugin_responses = pm.run_plugins(marvin_reply)
    if plugin_responses:
        for response in plugin_responses:
            chat_history.append({
                "role": "system",
                "content": response.strip()
            })
            chat_history.append({
                "role": "user",
                "content": f"marvin, the plugin returned this:\n{response.strip()}\n. Please summarize it within a few sentences, answering my question:\n{message}"
            })
            
            yield response
            
            summary_stream = llm.create_chat_completion(messages=chat_history,
                                        stream=True,
                                        max_tokens=1000,
                                        temperature=0.3,
                                        top_p=0.7,
                                        top_k=40
                                    )
            yield "__END__"
            summary = ""
            for chunk in summary_stream:
                token = chunk["choices"][0]["delta"].get("content", "")
                summary += token
                yield f"__APPEND__{token}"
            yield "__END__"
            
            chat_history.append({
                "role": "assistant",
                "content": summary.strip()
            })
    if len(chat_history) > (2 * max_history + 1):
        chat_history = [chat_history[0]] + chat_history[-(max_history * 2):]
    
    with open(history_path, "w") as file:
        json.dump(chat_history, file, indent=2)


def test_tokens(dummy):
    chat_history = [ {
    "role": "system",
    "content": "2025-07-11 13:02:10.556991"
  },
  {
    "role": "user",
    "content": "marvin, the plugin returned this: 2025-07-11 13:02:10.556991\n. Please summarize it within a few sentences, taking into account what the I previously asked for."
  }]
    reply = "This is a test of the WEB UI's token streaming capabilities [WRITE_PY]print('hhi')[/WRITE_PY] [TIME] [WEATHER] singapore [/WEATHER]"
    for token in reply.split():
        time.sleep(0.5) 
        yield f"__APPEND__{token} "
    yield "__END__"
    plugin_responses = pm.run_plugins(reply)
    if plugin_responses:
        for response in plugin_responses:
            yield response
            
    yield "test system thingy"
            

        

        
        
        


