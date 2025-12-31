import os
from dotenv import load_dotenv

from strands import Agent, tool

from strands_tools import calculator
from strands_tools.agent_core_memory import AgentCoreMemoryToolProvider

from .math_prompt import MATH_ASSISTANT_SYSTEM_PROMPT

from utils import bedrock_model, ollama_model
from memory import MemoryHookProvider

from bedrock_agentcore.memory import MemoryClient

import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

client = MemoryClient(region_name=os.getenv("REGION_NAME"))
memory_name = os.getenv("MEMORY_NAME")
memory_id = os.getenv("MEMORY_ID")
memory_strategy_id = os.getenv("MEMORY_STRATEGY_ID")


math_memory_hooks = MemoryHookProvider(memory_id=memory_id, client=client)


@tool
def math_agent(query: str) -> str:
    """This is responsible for handling math questions.

    Args:
        query (str): A math questions or problem from the user.

    Returns:
        str: A detailed math answer with explanation of the steps taken to derive the answer.
    """

    full_query = f"Please solve the following math problem, show all your steps and explain the concepts clearly: {query}"
    try:
        logging.info("Routed to math agent")

        session_id = os.getenv("SESSION_ID")

        actor_id = "math-subagent"
        math_namespace = (
            f"/strategies/{memory_strategy_id}/actors/{actor_id}/sessions/{session_id}"
        )

        provider_math = AgentCoreMemoryToolProvider(
            memory_id=memory_id,
            actor_id=actor_id,
            session_id=session_id,
            region=os.getenv("REGION_NAME"),
            namespace=math_namespace,
        )

        math_memory_hooks.set_actor_id(actor_id=actor_id)
        math_memory_hooks.set_session_id(session_id=session_id)

        math_agent = Agent(
            model=bedrock_model,
            system_prompt=MATH_ASSISTANT_SYSTEM_PROMPT,
            # callback_handler=None,
            # .tools method from provider returns a list
            tools=[calculator] + provider_math.tools,
            hooks=[math_memory_hooks],
        )

        response = math_agent(full_query)
        text_response = str(response)

        if len(text_response) > 0:
            return text_response

        return "I was unable to solve thisproblem. Please check that the question is phrased properly."

    except Exception as e:
        logging.error(
            f"An error occured in processing this query: {str(e)}", exc_info=True
        )
        return f"An error occured in processing this query: {str(e)}"
