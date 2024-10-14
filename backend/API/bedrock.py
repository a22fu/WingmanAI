import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
import uuid
import json
from tests.prompt_tests_suite import create_team_prompts, edit_team_prompts, valorant_news_stats_prompts, other_prompts
from prompt_templates import *


# load_dotenv()
# agent_role = os.environ.get('AGENT_ROLE')


class VctClient():
    def __init__(self,
                 region_name="us-east-1"):
        self.region_name = region_name
        self.agentId = "VMPZXQYLQ0"
        self.agentAlias = "T076UHLG01"

    def return_runtime_client(self, run_time=True) -> BaseClient:
        if run_time:
            bedrock_client = boto3.client(
                service_name="bedrock-agent-runtime",
                region_name=self.region_name)
        else:
            bedrock_client = boto3.client(
                service_name="bedrock-agent",
                region_name=self.region_name)

        return bedrock_client

    def invoke_bedrock_agent(self,
                             agent_id,
                             agent_alias_id,
                             session_id,
                             prompt=None):

        completion = ""
        traces =[]
        try:
            bedrock_client = self.return_runtime_client(run_time=True)
            response = bedrock_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt,
                sessionState={
        'knowledgeBaseConfigurations': [
            {
                'knowledgeBaseId': 'MMUTW03GYI',
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                       
                        'numberOfResults': 25,
                    }
                }
            },
        ]
                }
            )
            for event in response.get("completion"):
                try:
                    trace = event["trace"]
                    traces.append(trace['trace'])
                except KeyError:
                    chunk = event["chunk"]
                    completion = completion + chunk["bytes"].decode()
                except Exception as e:
                    print(e)

        except ClientError as e:
            print(e)

        return completion
    
    def categorize_input(self, input):
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Set the model ID, e.g., Claude 3 Haiku.
        model_id = "anthropic.claude-instant-v1"
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": input + CATEGORIZE_TEMPLATE_STR}],
                }
            ],
        }
        request = json.dumps(native_request)
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        response_text = model_response["content"][0]["text"]
        return response_text

    def create_team(self, input, uuid):
        raw = self.invoke_bedrock_agent(agent_id=self.agentId,
                                                agent_alias_id=self.agentAlias,
                                                session_id= uuid,
                                                prompt = input + CREATE_TEAM_TEMPLATE_STR)
        return self.invoke_bedrock_agent(agent_id=self.agentId,
                                                    agent_alias_id=self.agentAlias,
                                                    session_id=uuid,
                                                    prompt = PARSE_CREATE_TEAM_TEMPLATE_STR + raw)
    def edit_team(self, input, uuid):
        raw = self.invoke_bedrock_agent(agent_id=self.agentId,
                                                agent_alias_id=self.agentAlias,
                                                session_id= uuid,
                                                prompt = input + EDIT_TEAM_TEMPLATE_STR)
        return self.invoke_bedrock_agent(agent_id=self.agentId,
                                                    agent_alias_id=self.agentAlias,
                                                    session_id=uuid,
                                                    prompt = PARSE_EDIT_TEAM_TEMPLATE_STR + raw)
 

if __name__ == "__main__":
    bedrock_client = VctClient()
    # bedrock_runtime_client = bedrock_client.return_runtime_client()

    # agents = bedrock_client.list_agents()
    # print(agents)

    # response = bedrock_client.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
    #                                                agent_alias_id="T076UHLG01",
    #                                                session_id="1234",
    #                                                prompt = "create a team of 3 gc players and 2 international players`\n" + CREATE_TEAM_TEMPLATE_STR)
    # response = bedrock_client.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
    #                                                agent_alias_id="T076UHLG01",
    #                                                session_id="1234",
    #                                                prompt = PARSE_TEAM_TEMPLATE_STR + response)
    # for x in create_team_prompts:
    #     print(x)
    #     response = bedrock_client.categorize_input(x)
    #     print(response)

    # for x in edit_team_prompts:
    #     print(x)
    #     response = bedrock_client.categorize_input(x)
    #     print(response)
    # for x in valorant_news_stats_prompts:
    #     print(x)
    #     response = bedrock_client.categorize_input(x)
    #     print(response)
    # for x in other_prompts:
    #     print(x)
    #     response = bedrock_client.categorize_input(x)
        
        
