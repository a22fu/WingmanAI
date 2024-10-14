from flask import Flask, request, jsonify
from API.bedrock import VctClient  # Import your class
from flask_cors import CORS

import uuid
app = Flask(__name__)

CORS(app)

@app.route('/build_team', methods=['POST'])
def build_team():
    data = request.get_json()



    if not data or 'parameters' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    team_builder = VctClient()

    category = team_builder.categorize_input(data)
    sessionId = str(uuid.uuid4())
    match category:
        case "1":
            # Create team
            parameters = data['parameters']

            result = team_builder.create_team(parameters, sessionId)

            return result
        case "2":
            # Edit team
            return "Not found"
        case "3":
            # Valorant Info
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