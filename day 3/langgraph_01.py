from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. El estado: lo que fluye por el grafo
class State(TypedDict):
    numero: int
    resultado: str

# 2. Nodos: funciones que reciben state y devuelven state parcial
def duplicar(state: State) -> dict:
    return {"numero": state["numero"] * 2}

def evaluar(state: State) -> dict:
    if state["numero"] > 10:
        return {"resultado": f"{state['numero']} es grande"}
    else:
        return {"resultado": f"{state['numero']} es pequeño"}

# 3. Construir el grafo
builder = StateGraph(State)
builder.add_node("duplicar", duplicar)
builder.add_node("evaluar", evaluar)

builder.set_entry_point("duplicar")
builder.add_edge("duplicar", "evaluar")
builder.add_edge("evaluar", END)

graph = builder.compile()

# 4. Invocar
resultado = graph.invoke({"numero": 3, "resultado": ""})
print(resultado)

resultado2 = graph.invoke({"numero": 7, "resultado": ""})
print(resultado2)