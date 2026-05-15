import anthropic
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Manuel\Desktop\sap-ai-journey\.env")

client = anthropic.Anthropic()

tools = [
    {
        "name": "get_material_stock",
        "description": "Devuelve el stock disponible de un material SAP",
        "input_schema": {
            "type": "object",
            "properties": {
                "material_id": {"type": "string", "description": "Número de material SAP"}
            },
            "required": ["material_id"]
        }
    }
]

messages = [
    {"role": "user", "content": "¿Cuánto stock hay del material 4500?"}
]

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

tool_call = response.content[0]
material_id = tool_call.input["material_id"]

stock_mock = {"material_id": material_id, "stock": 342, "unidad": "UN"}

messages.append({"role": "assistant", "content": response.content})
messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": tool_call.id,
            "content": str(stock_mock)
        }
    ]
})

respuesta_final = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print(respuesta_final.content[0].text)