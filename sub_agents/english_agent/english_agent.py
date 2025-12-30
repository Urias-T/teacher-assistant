import os
from dotenv import load_dotenv

from utils import bedrock_model, ollama_model
from memory import MemoryHookProvider

from bedrock_agentcore.memory import MemoryClient

from strands import Agent, tool
from strands.hooks import HookRegistry

from strands_tools.agent_core_memory import AgentCoreMemoryToolProvider

from .english_prompt import ENGLISH_ASSISTANT_SYSTEM_PROMPT

import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

client = MemoryClient(region_name=os.getenv("REGION_NAME"))
memory_name = os.getenv("MEMORY_NAME")
memory_id = os.getenv("MEMORY_ID")
memory_strategy_id = os.getenv("MEMORY_STRATEGY_ID")
session_id = os.getenv("SESSION_ID")

english_memory_hooks = MemoryHookProvider(memory_id=memory_id, client=client)

english_memory_hooks.register_hooks(registry=HookRegistry)


@tool
def english_agent(query: str) -> str:
    """This is responsible for handling questions involving writing/ literature/ grammar

    Args:
        query (str): The user's English language/ literature/ writing question

    Returns:
        str: A helpful response addressing the user's query.
    """

    formatted_query = f"Analyze and respond to this English language query {query}"

    try:
        logging.info("Routed to the english agent")

        actor_id = "english-subagent"
        english_namespace = (
            f"/strategies/{memory_strategy_id}/actors/{actor_id}/sessions/{session_id}"
        )

        provider_english = AgentCoreMemoryToolProvider(
            memory_id=os.getenv("MEMORY_ID"),
            actor_id=actor_id,
            session_id=os.getenv("SESSION_ID"),
            region=os.getenv("REGION_NAME"),
            namespace=english_namespace,
        )

        english_agent = Agent(
            model=bedrock_model,
            system_prompt=ENGLISH_ASSISTANT_SYSTEM_PROMPT,
            # callback_handler=None,
            tools=provider_english.tools,  # .tools method from provider returns a list
            hooks=[english_memory_hooks],
        )

        response = english_agent(formatted_query)

        text_response = str(response)

        if len(text_response) > 0:
            return text_response

        return "I was unable to analyze this English question. Please rephrase and provide more context."

    except Exception as e:
        logging.error(
            f"An error occured in processing the English query: {str(e)}", exc_info=True
        )
        return f"An error occured in processing the English query: {str(e)}"
