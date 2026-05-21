# Proyecto 02 — Multi-tool SAP Agent (mock)

Agent that queries SAP stock, purchase orders, and pricing using mock data. Claude autonomously chains tools to answer complex queries.

## What it does
- `get_material_stock(material_number)` — stock by plant
- `get_purchase_order(po_number)` — PO status and details
- `get_material_price(material_number)` — standard price
- `find_purchase_orders_by_material(material_number)` — PO lookup by material (simulates EKPO query)

## Key behavior
Claude chains tools without being told to. Example: "Is MAT-002 in stock? If not, is there an open PO?" triggers stock check → material-to-PO lookup → PO detail, all autonomously.

## Stack
- LangGraph `create_react_agent`
- Claude Haiku via `langchain-anthropic`
- Mock data simulating SAP MM module

## Run
```bash
python agent.py
```

## Next
Proyecto 03 — real SAP connection via pyrfc