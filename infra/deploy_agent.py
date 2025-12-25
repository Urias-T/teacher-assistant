import boto3
import os

from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

account_id = os.getenv("ACCOUNT_ID")

client = boto3.client("bedrock-agentcore-control")

response = client.create_agent_runtime(
    agentRuntimeName="teacher_assistant",
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
