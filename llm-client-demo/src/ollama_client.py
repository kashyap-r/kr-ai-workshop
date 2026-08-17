from ollama import chat 
response = chat (model="qwen3:8b",
                 messages=[
                     {
                        "role": "user", 
                        "content": "Explain vector databases to me like I'm five."
                     }
                 ])

print(response.message.content)

"""
Prompt 1: "Tell me something interesting about AI"

Prompt 2: 
You are a helpful AI assistant.

Answer the user's question concisely.

User question:
Tell me something fun today

"""