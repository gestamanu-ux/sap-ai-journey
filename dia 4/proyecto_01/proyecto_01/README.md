# Proyecto 01 — SAP Stock Agent (mock)

Agent that queries SAP material stock using mock data. Built with LangGraph ReAct + Claude Haiku.

## What it does
- Exposes a mock SAP tool: `get_material_stock(material_number)`
- Claude autonomously decides when and how to call it
- Handles multi-step queries (check two materials, compare them)

## Stack
- LangGraph `create_react_agent`
- Claude Haiku via `langchain-anthropic`
- Mock data simulating SAP plant stock

## Run
```bash
python agent.py
```

## Next
Proyecto 02 — multiple mock SAP tools (stock + purchase orders + pricing)