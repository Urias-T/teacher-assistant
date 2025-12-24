from utils import ollama_model

from strands import Agent, tool

from .english_prompt import ENGLISH_ASSISTANT_SYSTEM_PROMPT

import logging

logging.basicConfig(level=logging.INFO)


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

        english_agent = Agent(
            model=ollama_model,
            system_prompt=ENGLISH_ASSISTANT_SYSTEM_PROMPT,
            # callback_handler=None
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
