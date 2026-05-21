import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# --- Mock SAP tool ---
@tool
def get_material_stock(material_number: str) -> str:
    """Returns current stock for a given SAP material number."""
    mock_data = {
        "MAT-001": "450 units in plant 1000",
        "MAT-002": "0 units — stockout",
        "MAT-003": "1200 units in plant 2000",
    }
    return mock_data.get(material_number, f"Material {material_number} not found in system.")

# --- Agent ---
model = ChatAnthropic(model="claude-haiku-4-5-20251001")
agent = create_react_agent(model, tools=[get_material_stock])

def run(query: str):
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print(result["messages"][-1].content)

if __name__ == "__main__":
    run("What is the stock for material MAT-002?")
    run("Check stock for MAT-001 and MAT-003 and tell me which has more.")