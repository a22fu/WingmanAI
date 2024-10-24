# WingmanAI
The Wingman chatbot creates a team and provides insights on each player's role, as well as modifies based on suggestions provided by the user. Our chatbot is powered by AWS Bedrock to provide live insights, recommendations and answers to users.

**Link to project:** https://vcthack.onrender.com/

## How It's Made:

**AWS Tools Used**: AWS bedrock (Anthropic Claude Sonnet 3.5, Anthropic Claude Instant v1), S3 Knowledge base storage, AWS Athena Database. 

**Frontend tools used:** React.js, Javascript, HTML/CSS

**Backend tools used:** Flask/boto3, Python, hosted on render.com

### Summary

Wingman was built with a Python and Flask backend along with a React.js frontend. The frontend provides an user friendly interface for the chatbot, where users can drag and drop their favourite VALORANT pros into the team slot, showcasing their custom team that they built along with the AI chatbot. To communicate with the chatbot, the app is equipped with a messaging area to send any prompts. The chatbot responds with a text message, showcasing the team that it created then updates the UI to display the new team that they created. Entering a prompt into the chat sends an API call to the backend, where it uses NLP to translate the message to something that the AWS bedrock model understands. After the message is classified, the backend retrieves relevant data from previous tournaments (on vlr.gg) for this query and sends it to AWS Bedrock to create the best possible team based on the statistics. It can also respond to user questions about the team, players, or justification for any choices and edit the team based on user request as well.

## Detailed writeup:

### Introduction 

The vision for our project from the beginning was to create a VCT LLM helper that was simple and appealing to users. We had two major goals, training the LLM to a level where it could handle all necessary requests, and implementing a responsive UI that makes users feel like they are interacting with a helpful assistant. We wanted our frontend to be one that is simple to use and captures the essence of creating a fantasy professional team with friends.  

### Data gathering and processing. 

Our process began with deciding what data would be important to build an effective team, deciding on two main categories, individual performance, and team synergy. 

To analyze individual performances, we used the stats of a player over a year of their most recent professional games, such as kills per round, average damage per round, and their recent tournament performances. To gather such data, we webscraped the vlr.gg tournament records and recorded their stats for each game within each tournament for the past year, finding the average over all their games. With 10+ statistics available, it became difficult for us, or a base LLM, to weigh the importance of each and make an informed decision. Anthropic Claude Sonnet 3 would choose one stat as justification and ignore the rest or use stats that would not be as important for analysis. Luckily, vlr.gg provides an individual rating score for each player in a match which is a cumulative weighted scoring for each player which considers a variety of stats, such as kills, even considers the impact of those kills within the round. This would be done for each agent that they played. 

Analyzing team synergy would be a bit more complicated as it is hard to represent statistically what makes a team work together, but we decided that role coverage, and having similar, but also balanced playstyles on a team would be our two main metrics. Since we already collected agent data, we just had to find a measure for different playstyles for each player. We decided on assigning an array of stats to corresponding playstyles, e.g., aggressive player: high first blood per round, plays duelists and supportive player: high assists per round, plays sentinels and controllers, etc. 

Our model also has access to an AWS Athena SQL table, with a list of players and overall stats for the past 90 days, which it accesses by creating an SQL query based on the user input if they request an accessible statistic. 

### Model training 

To train our model, we decided to use the base model of Anthropic Claude Sonnet 3.5. We considered fine-tuning but decided it would not work as well with the open-ended prompts. This is why we decided to focus on refining a knowledge base to maximize information retrieval quality and speed. Our knowledge base consists of two large directories of team and player data, with each separate team and player being split into its own file to prevent split chunking. Each file contains the corresponding stats and data gathered above, but turned into a narrative format, since the vector search used by AWS is much better at retrieving text-based information rather than structured csv data, or tables. The narratives would include the players' name as many times as possible, and include short, but succinct sentences to mimic answers to prompts we were expecting.  

Since there are thousands of players and teams with thousands of chunks to parse through, the LLM was not particularly accurate parsing through such a high volume of information. We added a metadata file for each player, listing their name, region, and league, which drastically increased chunk retrieval speed and accuracy. Finally, a last addition to the dataset was a document titled which included a summary of all the roles and features you would want in a typical team comp, e.g. smokes, entries, offensive and defensive roles, an experienced IGL, synergistic playstyles, etc. This document would be included in every request to build a team to give our model a guide, rather than including it in a pre-prompt since we found it to be far more consistent and reduce token spend. 

### Prompting 

To get more specific responses, while still covering a large array of questions, we split our input into different prompt flows and process each differently.  

We have 5 main categories of inputs: 

1. Team building: a request to create a team given any set of parameters 

2. Team Improving: a request to change or update an existing team 

3. General VCT/Valorant Team related question 

4. A specific statistic related questions for a player 

5. Other/unrelated 

Each flow uses a variety of methods which we discovered to increase our output accuracy, speed and easy data separation once sent to the frontend. A strategy we found was effective was employing Anthropic Claude Instant v1 models for fast processing of data irrespective of our knowledge base, which will be referred to as helpers. For example, we use a helper to first classify the input into a separate category and call the respective prompt flow. A helper is also used to parse a filter from a user input to reduce the knowledge base size, for example, "create a VCT international team", will be sent into a helper which will create a JSON filter for international league players to be used in the prompt request. We also perform team creation in steps using these filters, by first having one helper reduce the potential pool of candidates by finding ~20 suitable players for the user request, and then the final model uses all its knowledge base info on just those 20 players to form a team of 5, ensuring a precise response. We found this process increases the "performance level" of our teams, while keeping them diverse and synergistic. We also use helpers to parse our output into sections that will be used in the frontend, such as dividing the five players chosen into an array so that they can be displayed. 

### Challenges and learnings 

The biggest challenge throughout the Hackathon was implementing or teaching the model on how to create a team that would be effective genuinely consider the provided data. Our process went through many changes, we even considered just using the LLM to filter through players and using a genetic algorithm to select the team. In the end, we created a web of prompts, knowledge base chunks and filters that would accurately be able to answer VCT related queries. Every decision in our methodology was made to solve a unique challenge that we ran into. The major takeaway in the data processing and design process was the effectiveness of proper modularization alongside dividing and conquering of huge datasets. We used many scraping, filtering, and data processing techniques just to minimize the amount of data that needed to be used by the model, enhancing its speed and performance. 

### Conclusion 
