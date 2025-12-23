from strands import Agent, tool
from strands_tools import calculator

from .math_prompt import MATH_ASSISTANT_SYSTEM_PROMPT

from utils import bedrock_model

import logging

logging.basicConfig(level=logging.INFO)


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

        math_agent = Agent(
            model=bedrock_model,
            system_prompt=MATH_ASSISTANT_SYSTEM_PROMPT,
            # callback_handler=None,
            tools=[calculator],
        )

        response = math_agent(full_query)
        text_response = str(response)

        if len(text_response) > 0:
            return text_response

        return "I was unable to solve thisproblem. Please check that the question is phrased properly."

    except Exception as e:
        logging.error(f"An error occured in processing this query: {str(e)}", exc_info=True)
        return f"An error occured in processing this query: {str(e)}"
