import os
import logging

from dotenv import load_dotenv

from bedrock_agentcore.memory import MemoryClient

from strands.hooks import AfterInvocationEvent, HookProvider, HookRegistry


logging.basicConfig(level=logging.INFO)  # Switch to INFO before pushing to prod...


load_dotenv()

client = MemoryClient(region_name=os.getenv("REGION_NAME"))
memory_name = os.getenv("MEMORY_NAME")
memory_id = os.getenv("MEMORY_ID")


class MemoryHookProvider(HookProvider):
    """Hook provider class for automatic memory management"""

    def __init__(self, memory_id: str, client: MemoryClient):
        self.memory_id = memory_id
        self.client = client

    def set_actor_id(self, actor_id: str) -> None:
        self.actor_id = actor_id

    def set_session_id(self, session_id: str) -> None:
        self.session_id = session_id

    def after_invocation(self, event: AfterInvocationEvent):
        """Save conversation after agent response"""
        logging.info("Triggered save memory hook")
        try:
            messages = event.agent.messages
            if len(messages) >= 2:
                user_msg = None
                assistant_msg = None

                logging.debug(f"MESSAGES: {str(messages)}")

                for msg in reversed(messages):
                    if msg["role"] == "assistant" and not assistant_msg:
                        assistant_msg = msg["content"][0]["text"]
                    elif (
                        msg["role"] == "user"
                        and not user_msg
                        and "toolResult" not in msg["content"][0]
                    ):
                        user_msg = msg["content"][0]["text"]
                        break

                logging.info(f"USER MSG: {str(user_msg)}")
                logging.info(f"ASSISTANT MSG: {str(assistant_msg)}")

                if user_msg and assistant_msg:
                    actor_id = self.actor_id
                    session_id = self.session_id

                    logging.debug(f"ACTOR_ID: {actor_id}")
                    logging.debug(f"SESSION_ID: {session_id}")

                    if not actor_id or not session_id:
                        logging.warning(
                            "There's no actor_id or session_is in agent state"
                        )
                        return

                    self.client.create_event(
                        memory_id=self.memory_id,
                        actor_id=actor_id,
                        session_id=session_id,
                        messages=[(user_msg, "USER"), (assistant_msg, "ASSISTANT")],
                    )

                    logging.info("Saved conversation to memory")

        except Exception as e:
            logging.error(f"Failed to save conversation to memory: {str(e)}")

    def register_hooks(self, registry: HookRegistry):
        """Register memory hooks"""
        registry.add_callback(AfterInvocationEvent, self.after_invocation)
        logging.info("Memory hooks registered")
