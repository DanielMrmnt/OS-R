import os
from zai import ZaiClient
import datetime

date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
api_key = os.getenv("AI_API_KEY")
client = ZaiClient(api_key=api_key)

MODEL = "glm-4.7-flash"
messages = [
    {"role": "system", "content": "Tu es un assistant utile."},
]

def chat(user_text):
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )

    reply = ""
    choice = response.choices[0]
    
    if hasattr(choice, "message") and hasattr(choice.message, "content"):
        reply = choice.message.content
    elif hasattr(choice, "content"):
        reply = choice.content
        
    if not reply:
        reply = "[Pas de réponse de l'assistant]"

    MAX_MESSAGES = 10
    messages[:] = messages[-MAX_MESSAGES:]
    messages.append({"role": "assistant", "content": reply})
    return reply

filename = f"conversation_du_{date}.md"
with open(filename, "x", encoding="utf-8") as f: 
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("Fin de la conversation.")
            break
        f.write(f"You : {user_input}\n")
        answer = chat(user_input)
        print("Assistant:", answer)
        f.write(f"Assistant: {answer}\n")
    