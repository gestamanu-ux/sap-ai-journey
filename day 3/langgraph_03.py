from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatAnthropic(model="claude-haiku-4-5-20251001")

def get_stock(material_id: str) -> str:
    """Consulta el stock de un material en SAP."""
    stocks = {"MAT001": 150, "MAT002": 0, "MAT003": 42}
    qty = stocks.get(material_id, -1)
    if qty == -1:
        return f"Material {material_id} no encontrado"
    return f"Material {material_id}: {qty} unidades en stock"

def get_price(material_id: str) -> str:
    """Consulta el precio de venta de un material en SAP."""
    prices = {"MAT001": 29.99, "MAT002": 149.00, "MAT003": 5.50}
    price = prices.get(material_id)
    if not price:
        return f"Material {material_id} no encontrado"
    return f"Material {material_id}: precio {price} EUR"

agent = create_react_agent(model, tools=[get_stock, get_price])

result = agent.invoke({
    "messages": [{"role": "user", "content": "¿Cuál es el precio de MAT001 y cuánto stock hay de MAT003?"}]
})

for msg in result["messages"]:
    print(type(msg).__name__, "→", msg.content)
    print("---")