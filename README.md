# VCTHack
The VCTHack chatbot creates a team and provides insights on each player's role, as well as modify based on suggestions provided by the user. 

**Link to project:** https://vcthack.onrender.com/

## How It's Made:

**Tech used:** AWS Bedrock, React.js, Flask, Javascript, HTML/CSS, Python 

VCTHack was built with a Python and Flask backend along with a React.js frontend. The frontend provides an user friendly interface for the chatbot, where users can drag and drop their favourite VALORANT pros into the team slot, showcasing their custom team that they built along with the AI chatbot. To communicate with the chatbot, the app is equipped with a messaging area to send any prompts. The chatbot responds with a text message, showcasing the team that it created then updates the UI to display the new team that they created. Entering a prompt into the chat sends an API call to the backend, where it uses NLP to translate the message to something that the AWS bedrock model understands. After the message is classified, the backend retrieves relevant data from previous tournaments (on vlr.gg) for this query and sends it to AWS Bedrock to create the best possible team based on the statistics. 

## What can the chatbot do:
### Support for the following VALORANT team submissions:
- Professional: Build a team with pro players (VCT International) only
- Semi-Professional: Build a team with semi-pro (VCT Challengers) players only
- VCT Game Changers: Build a team with VCT Game Changers players only
- Mixed-Gender: Build a team with at least 2 players from an underrepresented group (ex. Game Changers)
- Cross-Regional: Build a team with players from 3+ regions
- Rising Star: Build a team that includes at least two semi-professional players (VCT Challengers or VCT Game Changers)

### For each team composition, the model can:
- Answer questions about player performance with specific agents (in-game playable characters)
- Assign roles to players on the team and explain their contribution
  - Offensive vs. defensive roles
  - Category of in-game playable character / agent (duelist, sentinel, controller, initiator)
- Assign a team IGL (team leader, primary strategist and shotcaller)
- Provide insights on team strategy and hypothesize team strengths and weaknesses

## Example prompts:
- "Build a team using only players from VCT Game Changers. Assign roles to each player and explain why this composition would be effective in a competitive match."

video prompt here

- "Build a team with players from at least three different regions. Assign each player a role and explain the benefits of this diverse composition."

video prompt here

