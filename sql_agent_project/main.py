from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


# =========================
# 1. AGENT STATE (MEMORY)
# =========================

class AgentState(TypedDict):
    # Stores conversation messages
    messages: Annotated[list, add_messages]

    # Counts SQL retry attempts
    retry_count: int


# =========================
# 2. DATABASE SCHEMA
# =========================

db_schema = """
Table: Sales
Columns:
- id (INT)
- product_name (TEXT)
- amount (FLOAT)
- sale_date (DATE)
"""


# =========================
# 3. PLANNER NODE (LLM)
# =========================

def generate_query(state: AgentState):
    """
    Pretend LLM that generates SQL.
    Later you will replace this with OpenAI.
    """

    sql_query = "SELECT SUM(amount) FROM Sales;"

    return {
        "messages": [
            {"role": "assistant", "content": sql_query}
        ],
        "retry_count": state.get("retry_count", 0)
    }


# =========================
# 4. EXECUTOR NODE
# =========================

def execute_query(state: AgentState):
    last_message = state["messages"][-1]
    sql_query = last_message.content  # IMPORTANT FIX

    print("Executing SQL:", sql_query)

    try:
        # Fake success for now
        return {
            "messages": [
                {"role": "assistant", "content": "Success: Query executed"}
            ],
            "retry_count": state.get("retry_count", 0)
        }

    except Exception as e:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Error: {str(e)}. Please fix the SQL."
                }
            ],
            "retry_count": state.get("retry_count", 0) + 1
        }


# =========================
# 5. BUILD THE GRAPH
# =========================

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", generate_query)
workflow.add_node("executor", execute_query)

# Define flow
workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")


# =========================
# 6. CONDITIONAL LOGIC
# =========================

def should_continue(state: AgentState):
    last_message = state["messages"][-1].content  # IMPORTANT FIX

    print("Retry count:", state["retry_count"])

    if "Error" in last_message and state["retry_count"] < 3:
        print("Retrying...\n")
        return "planner"

    print("Finished.\n")
    return END


workflow.add_conditional_edges(
    "executor",
    should_continue
)


# =========================
# 7. RUN THE AGENT
# =========================

app = workflow.compile()

initial_state = {
    "messages": [
        {"role": "user", "content": "What is the total sales amount?"}
    ],
    "retry_count": 0
}

result = app.invoke(initial_state)

print("\nFINAL RESULT:")
print(result)
