from enum import Enum

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from ai_travel_agency.graph.basic_tool_node import BasicToolNode
from ai_travel_agency.graph.llm_integrations import create_openai_integration
from ai_travel_agency.graph.state import State
from ai_travel_agency.graph.routers import route_tools
from ai_travel_agency.prompts import TOOLS_SYSTEM_PROMPT_FOR_WEBAPP, TOOLS_SYSTEM_PROMPT, RESULT_BUILDER_SYSTEM_PROMPT
from ai_travel_agency.tools.flights_search_tool import search_flights
from ai_travel_agency.tools.hotels_search_tool import search_hotels


class Mode(Enum):
    WebApp = 1
    Assistant = 2


def get_chat_system_prompt(mode: Mode):
    if mode == Mode.WebApp:
        return TOOLS_SYSTEM_PROMPT_FOR_WEBAPP
    return TOOLS_SYSTEM_PROMPT


def build_graph(mode: Mode, output_mermaid: bool = False):
    tools = [search_flights, search_hotels]
    tool_node = BasicToolNode(tools=tools)
    graph_builder = StateGraph(State)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_node("chatbot", create_openai_integration(system_prompt=get_chat_system_prompt(mode), tools=tools))

    graph_builder.add_conditional_edges(
        "chatbot", route_tools, {"tools": "tools", END: END})

    graph_builder.add_edge(START, "chatbot")

    if mode == Mode.WebApp:
        graph_builder.add_edge("tools", END)

    if mode == Mode.Assistant:
        graph_builder.add_node("result_builder", create_openai_integration(system_prompt=RESULT_BUILDER_SYSTEM_PROMPT))
        graph_builder.add_edge("tools", "result_builder")
        graph_builder.add_edge("result_builder", END)

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    if output_mermaid:
        print(graph.get_graph().draw_mermaid())

    return graph