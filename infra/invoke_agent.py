import boto3
import json
import os

from dotenv import load_dotenv

import uuid
import secrets

import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()


def generate_session_id() -> str:
    """This is for generating a session id using uuid

    Returns:
        str: the 32-character session ID
    """
    initial_uid = uuid.uuid4().hex  # only 32-characters
    extra_character = secrets.token_hex(1)[0]  # 1 extra character

    uid = initial_uid + extra_character  # 33-characters

    print(uid)
    hex_to_letter = str.maketrans("0123456789abcdef", "abcdefghijklmnop")
    print(hex_to_letter)
    session_id = uid.translate(hex_to_letter)
    print(session_id)

    return session_id


def invoke_model(user_prompt: str) -> str:
    """This function invokes the deployed agent with a user prompt.

    Args:
        user_prompt (str): The user prompt

    Returns:
        response (str): The agent response
    """
    agent_core_client = boto3.client(
        "bedrock-agentcore", region_name=os.getenv("REGION_NAME")
    )

    payload = json.dumps({"input": {"prompt": user_prompt}})

    response = agent_core_client.invoke_agent_runtime(
        agentRuntimeArn=os.getenv("AGENT_RUNTIME_ARN"),
        runtimeSessionId=generate_session_id(),
        payload=payload,
        qualifier="DEFAULT",
    )

    response_body = response["response"].read()
    response_data = json.loads(response_body)

    return response_data


if __name__ == "__main__":
    while True:
        try:
            user_prompt = input("\n> ")
            if user_prompt.lower() == "exit":
                print("Goodbye!")
                break

            response = invoke_model(user_prompt=user_prompt)

            print(response)

        except KeyboardInterrupt:
            print("\n\nExecution Interrupted. Exiting...")
            break

        except Exception as e:
            logging.error(f"An error occured: {str(e)}", exc_info=True)
            break
