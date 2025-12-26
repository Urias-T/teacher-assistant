import boto3
import os

from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

account_id = os.getenv("ACCOUNT_ID")

client = boto3.client("bedrock-agentcore-control")

runtimes = client.list_agent_runtimes().get("agentRuntimes", [])
existing_agent = next(
    (a for a in runtimes if a["agentRuntimeName"] == "teacher_assistant"), None
)

response = client.update_agent_runtime(
    agentRuntimeId=existing_agent["agentRuntimeId"],
    agentRuntimeArtifact={
        "containerConfiguration": {
            "containerUri": f"{account_id}.dkr.ecr.eu-west-1.amazonaws.com/teacher-assistant:latest"
        }
    },
    roleArn=f"arn:aws:iam::{account_id}:role/AgentRuntimeRole",
)


logging.info("Agent Runtime created successfully!")
logging.info(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
logging.info(f"Status: {response['status']}")
