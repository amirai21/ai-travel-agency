from logging import exception
from ai_travel_agency.graph.graph_builder import build_graph, Mode

graph = build_graph(mode=Mode.Assistant, output_mermaid=False)
config = {"configurable": {"thread_id": "1"}}


def stream_graph_updates(user_input: str):
    events = graph.stream(
        {"messages": [("user", user_input)]}, config, stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except exception as e:
        print(e)
        break