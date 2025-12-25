from fastapi import FastAPI, HTTPException
from strands import Agent

from pydantic import BaseModel

from typing import Dict, Any

from datetime import datetime, timezone, timedelta

from utils import bedrock_model, ollama_model

from sub_agents import math_agent, english_agent

from teacher_prompt import TEACHER_SYSTEM_PROMPT

import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI(title="Teacher Assistant Server", version="0.1.0")


teacher_agent = Agent(
    model=bedrock_model,
    system_prompt=TEACHER_SYSTEM_PROMPT,
    # callback_handler=None,
    tools=[math_agent, english_agent],
)


class InvocationRequest(BaseModel):
    input: Dict[str, Any]


class InvocationResponse(BaseModel):
    output: Dict[str, Any]


@app.post("/invocation", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    try:
        user_input = request.input.get("prompt", "")
        if not user_input:
            logging.error("No prompt given in input...")
            raise HTTPException(
                status_code=400, detail="No prompt provided. Please provide one."
            )

        response = teacher_agent(user_input)

        content = str(response)
        response = {
            "message": content,
            "timestamp": datetime.now(timezone.utc)
            .astimezone(timezone(timedelta(hours=1)))
            .isoformat(),
            "model": "teacher-assistant",
        }

        return InvocationResponse(output=response)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Agent processing failed: {str(e)}"
        )


@app.get("/ping")
async def ping():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
