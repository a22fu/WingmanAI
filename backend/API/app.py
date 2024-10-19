from flask import Flask, request, jsonify
from bedrock import VctClient  # Import your class
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
            result = team_builder.create_query(input, sessionId)
            return result
        # Failed
        case "5":
            return "Sorry I can't help you with that"
    return "Sorry I can't help you with that"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)