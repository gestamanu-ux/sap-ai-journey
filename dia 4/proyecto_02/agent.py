
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# --- Mock SAP tools ---
@tool
def get_material_stock(material_number: str) -> str:
    """Returns current stock for a given SAP material number."""
    data = {
        "MAT-001": "450 units in plant 1000",
        "MAT-002": "0 units — stockout",
        "MAT-003": "1200 units in plant 2000",
    }
    return data.get(material_number, f"Material {material_number} not found.")

@tool
def get_purchase_order(po_number: str) -> str:
    """Returns status and details of a SAP purchase order."""
    data = {
        "PO-1001": "Open — 500 units MAT-001, vendor V-200, delivery 2026-06-01",
        "PO-1002": "Closed — 200 units MAT-003, vendor V-105, delivered 2026-05-10",
        "PO-1003": "Blocked — 300 units MAT-002, vendor V-300, pending invoice verification",
        "PO-1004": "Open — 100 units MAT-002, vendor V-300, delivery 2026-06-15",
    }
    return data.get(po_number, f"Purchase order {po_number} not found.")

@tool
def get_material_price(material_number: str) -> str:
    """Returns the standard price of a SAP material."""
    data = {
        "MAT-001": "EUR 12.50 per unit (standard price, plant 1000)",
        "MAT-002": "EUR 8.00 per unit (standard price, plant 1000)",
        "MAT-003": "EUR 45.00 per unit (standard price, plant 2000)",
    }
    return data.get(material_number, f"No price found for {material_number}.")

@tool
def find_purchase_orders_by_material(material_number: str) -> str:
    """Finds all purchase orders for a given SAP material number."""
    data = {
        "MAT-001": ["PO-1001"],
        "MAT-002": ["PO-1003", "PO-1004"],
        "MAT-003": ["PO-1002"],
    }
    pos = data.get(material_number)
    if not pos:
        return f"No purchase orders found for {material_number}."
    return f"Purchase orders for {material_number}: {', '.join(pos)}"

# --- Agent ---
model = ChatAnthropic(model="claude-haiku-4-5-20251001")
agent = create_react_agent(model, tools=[get_material_stock, get_purchase_order, get_material_price, find_purchase_orders_by_material])

def run(query: str):
    print(f"\n>>> {query}")
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print(result["messages"][-1].content)

if __name__ == "__main__":
    run("Is MAT-002 in stock? If not, is there an open purchase order for it?")
    run("What is the total value of stock for MAT-001?")
    run("Give me a summary of PO-1003 and tell me the price of the material it references.")
