import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
import uuid
CREATE_TEAM_TEMPLATE_STR = """
Try to make the best team possible prioritizing:
1. Firstly, high ratings above 1.2 in tournaments
2. Secondly, high placements with teams in tournaments
3. Third, Having at least one of each agent role on the team, (duelist, controller, sentinel, initiator, flex(someone shown to play multiple roles)). 

you MUST return five unique players, make do if you can't find optimal choices

A team should should try to include as many of the following roles as possible and it should be considered a weakness if there isn't one
    "smokes": ["omen", "brimstone", "viper", "astra", "harbor", "clove"],
    "entry": ["reyna", "phoenix", "yoru", "iso"],
    "intel_gatherer": ["sova", "fade", "cypher","gekko","skye"],
    "lurker": ["cypher", "omen", "chamber", "yoru", "viper", "killjoy"],
    "flank_watch": ["killjoy", "cypher", "chamber","vyse"],
    "flash_initiator": ["skye", "kayo", "breach", "phoenix","reyna","gekko"],
    "movement_duelist": ["reyna", "raze", "neon", "jett", "yoru"]
    "controller": ["astra", "brimstone", "harbor", "omen", "viper", "clove"],
    "sentinel": ["chamber", "cypher", "killjoy", "sage", "vyse"],
    "duelist": ["jett", "neon", "phoenix", "raze", "reyna", "yoru", "iso"],
    "initiator": ["breach", "fade", "gekko", "kayo", "skye", "sova"]

Include a detailed explanation of each choice you made, and strengths and weaknesses of the team
do not under any circumstances mention search results or sources in the output
do not under any circumstances mention specific rating numbers or first contact per round, only say how well they are performing or their offensive vs defensive roles on the team.

"""
PARSE_TEAM_TEMPLATE_STR = """
You will receive an output from a Valorant team creator bot that either creates or edits a team composition or answers a general Valorant-related question. Your task is to parse the output and organize the information into distinct tags for further use in a program.

If the output is for creating or editing a team composition, it will include a list of players, strengths, weaknesses, and possibly new players if the team is being edited. Separate the output into the following categories:

[players]: This should include the final team of five players, reflecting any edits if new players were added or swapped. If no edits were requested, it will include the original five players.
[strengths]: A list or description of the team’s strengths.
[weaknesses]: A list or description of the team’s weaknesses.
[original_output]: The original output string from the Valorant team creator bot.
If the output is an answer to a general Valorant-related question, just return the output under the [general_response] tag, without separating it into the team composition structure.

Make sure that each section is wrapped in distinct exit tags and that only relevant sections are included. For example:

[players]
Player1, Player2, Player3, Player4, Player6
[/players]

[strengths]
Strong agent synergy, High fragging power
[/strengths]

[weaknesses]
Lack of experience on certain maps
[/weaknesses]

[original_output]
<Original bot output here>
[/original_output]

[general_response]
<For general Valorant answers, if applicable>
[/general_response]
If an edit was requested, ensure that [players] reflects the new final team with any edits included.
If any sections (such as weaknesses) are not relevant, you can omit those sections. The input is as follows: \n
"""

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

    def create_team(self, input, uuid):
        raw = self.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
                                                agent_alias_id="T076UHLG01",
                                                session_id= uuid,
                                                prompt = input + CREATE_TEAM_TEMPLATE_STR)
        return self.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
                                                    agent_alias_id="T076UHLG01",
                                                    session_id=uuid,
                                                    prompt = PARSE_TEAM_TEMPLATE_STR + raw)
 

if __name__ == "__main__":
    bedrock_client = VctClient()
    # bedrock_runtime_client = bedrock_client.return_runtime_client()

    # agents = bedrock_client.list_agents()
    # print(agents)

    response = bedrock_client.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
                                                   agent_alias_id="T076UHLG01",
                                                   session_id="1234",
                                                   prompt = "create a team of 3 gc players and 2 international players`\n" + CREATE_TEAM_TEMPLATE_STR)
    response = bedrock_client.invoke_bedrock_agent(agent_id="VMPZXQYLQ0",
                                                   agent_alias_id="T076UHLG01",
                                                   session_id="1234",
                                                   prompt = PARSE_TEAM_TEMPLATE_STR + response)
    print(response)
