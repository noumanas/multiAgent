from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from agent.router import run_agent
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()


@app.post("/agent")
def agent_endpoint(prompt: str, agentType: str = "tracks"):
    return StreamingResponse(run_agent(prompt, agentType), media_type="text/event-stream")