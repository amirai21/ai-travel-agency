import json

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from ai_travel_agency.data_types.user_input_request import UserInputRequest
from ai_travel_agency.graph.graph_builder import build_graph, Mode
from contextlib import suppress

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",  # React frontend running locally
    "https://your-production-domain.com"  # Replace with your domain
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # HTTP methods allowed (GET, POST, etc.)
    allow_headers=["*"],  # Headers allowed
)


_graph = build_graph(mode=Mode.WebApp, output_mermaid=False)

def derive_response_type(response: str):
    with suppress(json.JSONDecodeError):
        parsed = json.loads(response)
        if not isinstance(parsed, list) or len(parsed) < 1:
            return "message"

        first_offer = parsed[0]
        if not isinstance(first_offer, dict):
            return "message"
        if "type" in first_offer and first_offer["type"] == "hotel":
            return "hotels"
        if "flights" in first_offer:
            return "flights"
        return "message"

    return "message"



@app.post("/chat")
async def process_input(request: UserInputRequest):
    try:
        state = {"messages": [("user", request.user_input)]}
        config = {"configurable": {"thread_id": request.thread_id}}
        result = _graph.invoke(state, config=config)
        return {"response": result["messages"][-1].content,
                "response_type": derive_response_type(result["messages"][-1].content),
                "thread_id": request.thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)