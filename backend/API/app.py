from flask import Flask, request, jsonify
from bedrock import VctClient
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/build_team', methods=['POST'])
def build_team():
    data = request.get_json()
    input = data['parameters']['input']
    team = data['parameters']['current_team']
    # sessionId = str(uuid.uuid4())
    sessionId = data['parameters']['sessionId']
    # sessionId = "session1"
    team_builder = VctClient()



    if not data or 'parameters' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    category = team_builder.categorize_input(input)
    print(category)
    match category:
        case "1":
            result = team_builder.create_team(input, sessionId)
            return result
        case "2":
            result = team_builder.edit_team(input, team, sessionId)
            return result
        case "3":
            # Valorant Info
            result = team_builder.analyze_team(input, team, sessionId)
            return result
        case "4":
            result = team_builder.create_query(input)
            return result
        # Failed
        case "5":
            return "Sorry I can't help you with that"
    return "Sorry I can't help you with that"

@app.route('/change_team', methods=['POST'])
def change_team():
    data = request.get_json()
    old_team = data['parameters']['oldTeam']
    old_player = data['parameters']['oldPlayer']
    new_player = data['parameters']['newPlayer']
    team_builder = VctClient()
    prompt = ""
    print(old_team)
    if old_player and new_player:
        prompt = (
            f"Given the team: {', '.join(old_team)}, "
            f"analyzing the replacement of '{old_player}' with '{new_player}'. "
            "Please provide a list of strengths and potential challenges from making this replacement."
        )
    elif old_player:
        prompt = (
            f"Given the team: {', '.join(old_team)}, "
            f"analyze the impact of removing '{old_player}' from the team. "
            "Provide a list of strengths or potential challenges this change might bring."
        )
    elif new_player:
        prompt = (
            f"Given the team: {', '.join(old_team)}, "
            f"analyze the impact of adding '{new_player}' to the team. "
            "Provide a list of strengths and potential challenges this new addition might offer."
        )
    else:
        raise ValueError("Both oldPlayer and newPlayer cannot be empty.")
    old_team.append(old_player)
    old_team.append(new_player)
    return team_builder.change_team(prompt, old_team)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)