from strands import Agent

from utils import bedrock_model, ollama_model

from sub_agents import math_agent, english_agent

from teacher_prompt import TEACHER_SYSTEM_PROMPT

import logging

logging.basicConfig(level=logging.INFO)


teacher_agent = Agent(
    model=ollama_model,
    system_prompt=TEACHER_SYSTEM_PROMPT,
    # callback_handler=None,
    tools=[math_agent, english_agent],
)


if __name__ == "__main__":
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            response = teacher_agent(user_input)

            content = str(response)
            print(content)

        except KeyboardInterrupt:
            print("\n\nExecution Interrupted. Exiting...")
            break
        except Exception as e:
            logging.error(f"An error occured: {str(e)}", exc_info=True)
            # print(f"An error occured: {str(e)}")
            print("Please ask another question.")
