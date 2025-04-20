# lambda/bedrock_handler.py

import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    messages = body.get("messages", [])

    prompt = "\n\n".join(
        [f"{'Human' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in messages]
    ) + "\nAssistant:"

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 1024,
            "temperature": 0.7,
        })
    )

    result = json.loads(response["body"].read())
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"completion": result["completion"]})
    }
