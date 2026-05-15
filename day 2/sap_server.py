from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

app = Server("sap-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_stock",
            description="Devuelve el stock de un material en una planta SAP",
            inputSchema={
                "type": "object",
                "properties": {
                    "material": {"type": "string", "description": "Número de material"},
                    "planta":   {"type": "string", "description": "Código de planta"}
                },
                "required": ["material", "planta"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_stock":
        material = arguments["material"]
        planta   = arguments["planta"]
        stock_mock = {"material": material, "planta": planta, "stock": 42, "unidad": "UN"}
        return [TextContent(type="text", text=json.dumps(stock_mock))]

if __name__ == "__main__":
    import asyncio

    async def run():
        async with stdio_server() as (read, write):
            await app.run(read, write, app.create_initialization_options())

    asyncio.run(run())