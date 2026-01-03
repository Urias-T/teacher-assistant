import boto3
import os

from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

account_id = os.getenv("ACCOUNT_ID")

client = boto3.client("bedrock-agentcore-control")

agent_runtime_name = "teacher_assistant"

runtimes = client.list_agent_runtimes().get("agentRuntimes", [])
existing_agent = next(
    (a for a in runtimes if a["agentRuntimeName"] == agent_runtime_name), None
)

if existing_agent:
    logging.info(f"Updating existing agent with ID: {existing_agent['agentRuntimeId']}")
    response = client.update_agent_runtime(
        agentRuntimeId=existing_agent["agentRuntimeId"],
        agentRuntimeArtifact={
            "containerConfiguration": {
                "containerUri": f"{account_id}.dkr.ecr.eu-west-1.amazonaws.com/teacher-assistant:latest"
            }
        },
        networkConfiguration={"networkMode": "PUBLIC"},
        roleArn=f"arn:aws:iam::{account_id}:role/AgentRuntimeRole",
    )
else:
    logging.info("Deploying new agent runtime...")
    response = client.create_agent_runtime(
        agentRuntimeName=agent_runtime_name,
        agentRuntimeArtifact={
            "containerConfiguration": {
                "containerUri": f"{account_id}.dkr.ecr.eu-west-1.amazonaws.com/teacher-assistant:latest"
            }
        },
        networkConfiguration={"networkMode": "PUBLIC"},
        roleArn=f"arn:aws:iam::{account_id}:role/AgentRuntimeRole",
    )


logging.info("Agent Runtime created successfully!")
logging.info(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
logging.info(f"Status: {response['status']}")
