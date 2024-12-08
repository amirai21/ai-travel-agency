from collections.abc import Callable
from langchain_openai import ChatOpenAI
from ai_travel_agency.graph.state import State
from typing import List
from langchain.schema import SystemMessage


def create_openai_integration(
        system_prompt: str,
        tools: List[Callable] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0,
        max_retries: int = 2,
):
    llm = ChatOpenAI(model_name=model, temperature=temperature, max_retries=max_retries)

    if tools:
        llm = llm.bind_tools(tools)

    def llm_integration(state: State):
        system_message = SystemMessage(content=system_prompt)
        messages_history = [system_message] + state["messages"]
        return {"messages": [llm.invoke(messages_history)]}

    return llm_integration