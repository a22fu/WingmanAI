# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to generate a message with Anthropic Claude (on demand).
"""
import boto3
import json
import logging

from botocore.exceptions import ClientError

import geneticalg
from prompt_templates import CREATE_TEAM_TEMPLATE_STR, FILTER_INPUT_TEMPLATE_STR
import test_suite

class vctAgent:

    def __init__(self):
        # Prepare the tool configuration with the weather tool's specification
        # Create a Bedrock Runtime client in the specified AWS Region.
        self.bedrock_runtime = boto3.client(service_name='bedrock-runtime')
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        self.system_prompt = FILTER_INPUT_TEMPLATE_STR
        self.max_tokens = 1000
        self.anthropic_version = "bedrock-2023-05-31"
        self.body={
                "anthropic_version": self.anthropic_version,
                "max_tokens": self.max_tokens,
                "system": self.system_prompt,
                "messages": "",
                "tools": [geneticalg.get_genalg_spec()]
            }  
        

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)



    def generate_message(self, messages):

        self.body["messages"] = messages
        
        response = self.bedrock_runtime.invoke_model(body=json.dumps(self.body), modelId=self.model_id)
        response_body = json.loads(response.get('body').read())
    
        return response_body
    
    def handle_input(self, input_text):
        user_message =  {"role": "user", "content": input_text}
        messages = [user_message]
        response = self.generate_message(messages)

    def create_team_response(self, input_text):
        user_message =  {"role": "user", "content": input_text}
        self.body["system"] = CREATE_TEAM_TEMPLATE_STR
        messages = [user_message]

        response = self.generate_message(messages)
        response = self._process_model_response(response)
        return response
    
    def _process_model_response(
        self, model_response
    ):
        """
        Processes the response received via Amazon Bedrock and performs the necessary actions
        based on the stop reason.

        :param model_response: The model's response returned via Amazon Bedrock.
        :param conversation: The conversation history.
        :param max_recursion: The maximum number of recursive calls allowed.
        """

        if model_response["stop_reason"] == "tool_use":
            # If the stop reason is "tool_use", forward everything to the tool use handler
            return self._handle_tool_use(model_response)
    
    def _handle_tool_use(
        self, model_response
    ):
        """
        Handles the tool use case by invoking the specified tool and sending the tool's response back to Bedrock.
        The tool response is appended to the conversation, and the conversation is sent back to Amazon Bedrock for further processing.

        :param model_response: The model's response containing the tool use request.
        :param conversation: The conversation history.
        :param max_recursion: The maximum number of recursive calls allowed.
        """

        # Initialize an empty list of tool results
        tool_results = []

        # The model's response can consist of multiple content blocks
        for i in range(len(model_response["content"])):
            if model_response["content"][i]["type"] == "text":
                # If the content block contains text, print it to the console
                continue
            elif model_response["content"][i]["type"] == "tool_use":
                tool_response = self._invoke_tool(model_response["content"][i])

                # Add the tool use ID and the tool's response to the list of results
                
        return tool_response["content"]


    def _invoke_tool(self, payload):
        """
        Invokes the specified tool with the given payload and returns the tool's response.
        If the requested tool does not exist, an error message is returned.

        :param payload: The payload containing the tool name and input data.
        :return: The tool's response or an error message.
        """

        tool_name = payload["name"]
        if tool_name == "genetic_alg_tool":
            input_data = payload["input"]

            # Invoke the weather tool with the input data provided by
            with open("functions.txt", 'a') as f:
                f.write(input_data["filter_data"])
                f.write(input_data["satisfies_constraints"])
            response = geneticalg.genetic_algorithm(input_data["filter_data"], input_data["satisfies_constraints"])
        else:
            error_message = (
                f"The requested tool with name '{tool_name}' does not exist."
            )
            response = {"error": "true", "message": error_message}

        return {"toolUseId": payload["id"], "content": response}

def main():
    """
    Entrypoint for Anthropic Claude message example.
    """
    testAgent = vctAgent()
    for x in test_suite.create_team_prompts:
        with open("testdump.txt", 'a') as f:
            f.write("\nInput:" + x)
            f.write("\nOutput:")
            print(testAgent.create_team_response(x))
            print("prompt processsed")
        
    # for x in test_suite.create_team_prompts:
    #     ex = testAgent.create_team_response(x)
    #     with open("testdump.txt", 'a') as f:
    #         f.write("Input:" + x)
    #         f.write("Output:" + ex["content"][0]["text"])
    #   
    # 
    # 
    # for x in test_suite.edit_team_prompts:
    #     testAgent.handle_input(x)
    # for x in test_suite.valorant_news_stats_prompts:
    #     testAgent.handle_input(x)
    # for x in test_suite.other_prompts:
    #     testAgent.handle_input(x)

        #     bedrock_runtime = boto3.client(service_name='bedrock-runtime')

        #     model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        #     system_prompt = CREATE_TEAM_TEMPLATE_STR
        #     max_tokens = 1000

        #     # Prompt with user turn only.
        #     user_input = input("Create your valorant team:")

        #     user_message =  {"role": "user", "content": user_input}
        #     messages = [user_message]

        #     response = generate_message (bedrock_runtime, model_id, system_prompt, messages, max_tokens)
        #     constraints = json.loads(response["content"][0]["text"])
        #     dataset = geneticalg.get_data_set('vlr90.json', constraints)
        #     results = geneticalg.genetic_algorithm(dataset, constraints)
        #     print("Here is an example team:\n")
        #     zsum = 0
        #     for x in results:
        #         zsum += x["zscore"]
        #         print(x["player"])
        #     print(zsum)

        # except ClientError as err:
        #     message=err.response["Error"]["Message"]
        #     logger.error("A client error occurred: %s", message)
        #     print("A client error occured: " +
        #         format(message))

if __name__ == "__main__":
    main()

