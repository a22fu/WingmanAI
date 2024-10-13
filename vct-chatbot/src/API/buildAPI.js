import axios from 'axios';

function parseValorantOutput(output) {
    // Initialize variables
    let players = [];
    let strengths = '';
    let weaknesses = '';
    let originalOutput = '';
    let generalResponse = '';

    // Regular expressions to capture each section
    const playersRegex = /\[players\](.*?)\[\/players\]/s;
    const strengthsRegex = /\[strengths\](.*?)\[\/strengths\]/s;
    const weaknessesRegex = /\[weaknesses\](.*?)\[\/weaknesses\]/s;
    const originalOutputRegex = /\[original_output\](.*?)\[\/original_output\]/s;
    const generalResponseRegex = /\[general_response\](.*?)\[\/general_response\]/s;

    // Extract players array
    const playersMatch = output.match(playersRegex);
    if (playersMatch) {
        players = playersMatch[1].trim().split(',').map(player => player.trim());
    }

    // Extract strengths string
    const strengthsMatch = output.match(strengthsRegex);
    if (strengthsMatch) {
        strengths = strengthsMatch[1].trim();
    }

    // Extract weaknesses string
    const weaknessesMatch = output.match(weaknessesRegex);
    if (weaknessesMatch) {
        weaknesses = weaknessesMatch[1].trim();
    }

    // Extract original output string
    const originalOutputMatch = output.match(originalOutputRegex);
    if (originalOutputMatch) {
        originalOutput = originalOutputMatch[1].trim();
    }

    // Extract general response string (if present)
    const generalResponseMatch = output.match(generalResponseRegex);
    if (generalResponseMatch) {
        generalResponse = generalResponseMatch[1].trim();
    }

    // If a general response is present, return it directly
    if (generalResponse) {
        return {
            generalResponse: generalResponse
        };
    }

    // Return the parsed data
    return {
        "players": players,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "originalOutput": originalOutput
    };
}



async function buildTeam(user_input, setItems) {
    try {
        console.log(user_input); // Log for debugging; consider removing or using a logger in production

        // Send a POST request to the Flask API
        const response = await axios.post('http://localhost:5000/build_team', {
            parameters: user_input, // Ensure user_input is correctly structured
        });
        console.log(response)
        const data = parseValorantOutput(response.data)

        if (data["players"] != []){
            setItems(prevItems => {
                const oldItems = [
                ...prevItems.container1,
                ...prevItems.container2,
                ...prevItems.container3,
                ...prevItems.container4,
                ...prevItems.container5,
                ];
            
                return {
                container1: [data["players"][0]],
                container2: [data["players"][1]],
                container3: [data["players"][2]],
                container4: [data["players"][3]],
                container5: [data["players"][4]], 
            
                container6: [...prevItems.container6.filter(item => !data["players"].includes(item)), ...oldItems],
                };
            });
        }
        console.log(data)

        return data["originalOutput"]
    } catch (error) {
        console.error('Error:', error);
        throw error
    }
};

export default buildTeam;
