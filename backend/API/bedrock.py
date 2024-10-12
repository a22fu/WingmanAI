import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from prompt_templates import CREATE_TEAM_TEMPLATE_STR


# load_dotenv()
# agent_role = os.environ.get('AGENT_ROLE')


class VctClient():
    def __init__(self,
                 region_name="us-east-1"):
        self.region_name = region_name

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

    def list_agents(self):
        try:
            available_agents = []
            bedrock_client = self.return_runtime_client(run_time=False)
            agents = bedrock_client.list_agents()
            for agent in agents["agentSummaries"]:
                agent_status = agent["agentStatus"]
                if agent_status == "PREPARED":
                    agent_name = agent["agentName"]
                    available_agents.append(agent_name)
        except ClientError as e:
            print(e)
            raise
        else:
            return available_agents

    

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
                       
                        'numberOfResults': 20,
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

        return completion, traces


if __name__ == "__main__":
    bedrock_client = VctClient()
    # bedrock_runtime_client = bedrock_client.return_runtime_client()

    # agents = bedrock_client.list_agents()
    # print(agents)

    response,traces = bedrock_client.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
                                                   agent_alias_id="2THA8OIJOW",
                                                   session_id="session_01",
                                                   prompt = CREATE_TEAM_TEMPLATE_STR + "create a team of 5 VCT international players?")
    print(response)
