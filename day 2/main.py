import asyncio
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Manuel\Desktop\sap-ai-journey\.env")

async def main():
    # 1. Decirle al client cómo arrancar el server
    server_params = StdioServerParameters(
        command="python",
        args=["sap_server.py"]
    )

    # 2. Arrancar el server y conectar
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3. Pedir la lista de tools disponibles
            tools_result = await session.list_tools()

            # 4. Convertir al formato que entiende Anthropic
            tools_for_claude = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema
                }
                for t in tools_result.tools
            ]

            # 5. Llamar a Claude con las tools
            client = Anthropic()
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                tools=tools_for_claude,
                messages=[{
                    "role": "user",
                    "content": "¿Cuánto stock hay del material 4500012 en la planta MM01?"
                }]
            )

            print(response)

asyncio.run(main())