from flask import Flask, request, jsonify
from API.bedrock import VctClient  # Import your class
from flask_cors import CORS

import uuid
app = Flask(__name__)

CORS(app)

@app.route('/build_team', methods=['POST'])
def build_team():
    # Get the input data from the request
    data = request.get_json()

    # Ensure the data is valid and contains the necessary fields
    if not data or 'parameters' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Instantiate the TeamBuilder class with the data
    team_builder = VctClient()

    # Extract parameters from the incoming data
    parameters = data['parameters']

    # Call the method from the class to build the team using the parameters
    result = team_builder.create_team(parameters, str(uuid.uuid4()))

    # Return the result as a JSON response
    return result

if __name__ == '__main__':
    app.run(debug=True, port=5000)