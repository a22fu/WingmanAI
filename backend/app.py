from flask import Flask, request, jsonify
from API.bedrock import VctClient  # Import your class
from flask_cors import CORS

import uuid
app = Flask(__name__)

CORS(app)

@app.route('/build_team', methods=['POST'])
def build_team():
    data = request.get_json()
    input = data['parameters']['user_input']
    team = data['parameters']['current_team']
    # sessionId = str(uuid.uuid4())
    sessionId = "session1"
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
            result = team_builder.search_kb(input, sessionId)
            return "I'm a teapot"
        case "4":
            # Other
            return "I'm a teapot"
        # Failed
        case _:
            return "Something's wrong with the internet"
    # Extract parameters from the incoming data


if __name__ == '__main__':
    app.run(debug=True, port=5000)