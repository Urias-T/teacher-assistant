import boto3
import os

from dotenv import load_dotenv
from strands.models import BedrockModel
from strands.models.ollama import OllamaModel
from botocore.config import Config as BotocoreConfig

load_dotenv()


boto_config = BotocoreConfig(
    retries={"max_attempts": 3, "mode": "standard"}, connect_timeout=5, read_timeout=60
)


boto_session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)


bedrock_model = BedrockModel(
    model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.3,
    top_p=0.8,
    boto_client_config=boto_config,
    boto_session=boto_session,
)

ollama_model = OllamaModel(host="http://localhost:11434", model_id="llama3.1")
