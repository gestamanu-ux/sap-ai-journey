from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Modelo
model = ChatAnthropic(model="claude-haiku-4-5-20251001")

# Tool mock de SAP
def get_stock(material_id: str) -> str:
    """Consulta el stock de un material en SAP."""
    stocks = {"MAT001": 150, "MAT002": 0, "MAT003": 42}
    qty = stocks.get(material_id, -1)
    if qty == -1:
        return f"Material {material_id} no encontrado"
    return f"Material {material_id}: {qty} unidades en stock"

# Grafo prebuilt: Claude + tools en un ciclo ReAct
agent = create_react_agent(model, tools=[get_stock])

# Invocar
result = agent.invoke({
    "messages": [{"role": "user", "content": "¿Cuánto stock hay de MAT002 y MAT003?"}]
})

# El último mensaje es la respuesta final de Claude
for msg in result["messages"]:
    print(type(msg).__name__, "→", msg.content)
    print("---")
