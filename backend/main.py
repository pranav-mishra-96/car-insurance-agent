import json
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from agent import build_agent

app = FastAPI(title="Car Insurance Agent")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build the agent once on startup
agent_executor = build_agent()


# Request shape
class ChatRequest(BaseModel):
    message: str


async def stream_response(message: str) -> AsyncIterator[str]:
    """Run the agent and stream SSE events back to the frontend.

    Three event types:
    - token: a chunk of the assistant response
    - tool_use: when the agent calls a tool
    - done: signals the stream is complete
    """
    try:
        async for event in agent_executor.astream_events(
            {"input": message},
            version="v1",
        ):
            kind = event["event"]

            # Stream tokens as they arrive
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    yield json.dumps({
                        "type": "token",
                        "content": chunk.content,
                    })

            # Emit tool use event when agent calls a tool
            elif kind == "on_tool_end":
                yield json.dumps({
                    "type": "tool_use",
                    "tool": event["name"],
                    "output": event["data"].get("output", ""),
                })

        # Signal stream is complete
        yield json.dumps({"type": "done"})

    except Exception as e:
        yield json.dumps({
            "type": "error",
            "content": str(e),
        })


@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint — streams agent response as SSE."""
    return EventSourceResponse(
        stream_response(request.message),
        media_type="text/event-stream",
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}