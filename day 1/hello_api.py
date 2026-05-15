import anthropic
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Manuel\Desktop\sap-ai-journey\.env")

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Di 'hola mundo' y nada más."}
    ]
)

print(message.content[0].text)