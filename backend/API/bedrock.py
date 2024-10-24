import os
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
import uuid
import time
import json
import awswrangler as wr  

# from API.prompt_templates import *
from prompt_templates import *


aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

class VctClient():
    
    def __init__(self,
                 region_name="us-east-1"):
        self.region_name = region_name
        self.agentId = "VMPZXQYLQ0"
        self.agentAlias = "T076UHLG01"
        self.model_id = "anthropic.claude-instant-v1"
        self.client = boto3.client("bedrock-runtime", 
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
)

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

    def invoke_instant(self, input):
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": input}],
                }
            ],
        }
        request = json.dumps(native_request)
        response = self.client.invoke_model(modelId=self.model_id, body=request)
        model_response = json.loads(response["body"].read())

        response_text = model_response["content"][0]["text"]
        return response_text

    def invoke_bedrock_agent(self,
                             agent_id,
                             agent_alias_id,
                             session_id,
                             prompt=None, 
                             filters = None):

        completion = ""
        traces =[]
        try:
            bedrock_client = self.return_runtime_client(run_time=True)
            retrievalconfig = {
                                'vectorSearchConfiguration': {

                                    'numberOfResults': 20,
                                }
                            }
            if filters:
                retrievalconfig["vectorSearchConfiguration"]["filter"] = filters
            response = bedrock_client.invoke_agent(
                agentId=agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=prompt,
                sessionState={
                    'knowledgeBaseConfigurations': [
                        {
                            'knowledgeBaseId': 'MMUTW03GYI',
                            'retrievalConfiguration': retrievalconfig
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
        return self.invoke_instant(input + CATEGORIZE_TEMPLATE_STR)

    def get_filters(self, input):
        return self.invoke_instant(GET_FILTERS_TEMPLATE_STR + input)

    def create_team(self, input, uuid):
        filters = json.loads(self.get_filters(input))
        time.sleep(60)
        player_list = self.invoke_bedrock_agent(agent_id=self.agentId,
                                                    agent_alias_id=self.agentAlias,
                                                   session_id=uuid + "2",
                                                   prompt = GATHER_TEAM_TEMPLATE_STR,
                                                   filters=filters)
        player_array = player_list.split(', ')

        # Add the guide
        player_array.append('meta')
        filtered_players = {
                    "in": {
                            "key": "player",
                            "value": player_array
                        }
                }
        time.sleep(60)

        raw = self.invoke_bedrock_agent(agent_id=self.agentId,
                                                        agent_alias_id=self.agentAlias,
                                                        session_id=uuid,
                                                        prompt = CREATE_TEAM_TEMPLATE_STR + input,
                                                        filters=filtered_players)
        print(raw)
        return self.invoke_instant(PARSE_CREATE_TEAM_TEMPLATE_STR + raw) + "\n[original_output]\n" + raw + "\n[/original_output]"
    
    def edit_team(self, input, current_team, uuid):
        print(self.describe_team(current_team) + input + EDIT_TEAM_TEMPLATE_STR)
        raw = self.invoke_bedrock_agent(agent_id=self.agentId,
                                                agent_alias_id=self.agentAlias,
                                                session_id= uuid,
                                                prompt = self.describe_team(current_team) + input + EDIT_TEAM_TEMPLATE_STR)
        print(raw)
        return self.invoke_instant(self.describe_team(current_team) + PARSE_EDIT_TEAM_TEMPLATE_STR + raw) + "\n[original_output]\n" + raw + "\n[/original_output]"
    
    def analyze_team(self, input, current_team, uuid):
        

        raw = self.invoke_bedrock_agent(agent_id=self.agentId,
                                                    agent_alias_id=self.agentAlias,
                                                    session_id=uuid,
                                                    prompt =KB_SEARCH_TEMPLATE_STR +  self.describe_team(current_team) + input)

        return self.invoke_instant(OUTPUT_CLEANER_TEMPLATE_STR + raw)
        
    def describe_team(self, team):
        num_empty_slots = 5 - len(team)
    
        team_description = ', '.join(team)
        if num_empty_slots == 5:
            return ""
        # Construct the output string based on empty slots
        if num_empty_slots > 0:
            return f"Given the team of Valorant professional players, {team_description}, with {num_empty_slots} empty slot(s),"
        else:
            return f"Given the team of Valorant professional players, {team_description}, "
    
    def create_query(self, input):
        query = self.invoke_instant(SEARCH_STATS_TEMPLATE_STR + input)
        df = wr.athena.read_sql_query(sql=query, database="default")
        return self.invoke_instant(input + SQL_QUERY_PARSER_TEMPLATE_STR +  str(df))

