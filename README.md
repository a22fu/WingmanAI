# VCTHack
The VCTHack chatbot creates a team and provides insights on each player's role, as well as modify based on suggestions provided by the user. 

**Link to project:** https://vcthack.onrender.com/

## How It's Made:

**Tech used:** AWS Bedrock, React.js, Flask, Javascript, HTML/CSS, Python 

VCTHack was built with a Python and Flask backend along with a React.js frontend. The frontend provides an user friendly interface for the chatbot, where users can drag and drop their favourite VALORANT pros into the team slot, showcasing their custom team that they built along with the AI chatbot. To communicate with the chatbot, the app is equipped with a messaging area to send any prompts. The chatbot responds with a text message, showcasing the team that it created then updates the UI to display the new team that they created. Entering a prompt into the chat sends an API call to the backend, where it uses NLP to translate the message to something that the AWS bedrock model understands. After the message is classified, the backend retrieves relevant data from previous tournaments (on vlr.gg) for this query and sends it to AWS Bedrock to create the best possible team based on the statistics. 

## What can the chatbot do:

### Example prompts:
- `Build a team with 2 NA players, 1 EU player and 2 KR players`

video prompt here

- `Build a team with Jing`

video prompt here

