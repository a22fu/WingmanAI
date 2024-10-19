import axios from 'axios';

import { v4 as uuidv4 } from 'uuid';
import playerdata from '../players/playerdata';
const uuid = uuidv4();

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
    }else{
        originalOutput = output
    }


    // Return the parsed data
    return {
        "players": players,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "originalOutput": originalOutput
    };
}



async function buildTeam(user_input, items, setItems) {
    try {
        console.log(user_input); // Log for debugging; consider removing or using a logger in production

        // Send a POST request to the Flask API
        const team = items.container1.concat(items.container2).concat(items.container3).concat(items.container4).concat(items.container5)
        console.log(team)
        console.log(uuid)
        const response = await axios.post('http://0.0.0.0:8000', {
            parameters: {
                input: user_input,
                current_team: team,
                sessionId: uuid,
            }
        });
        console.log(response)
        const data = parseValorantOutput(response.data)
        console.log(data)
        if (data["players"].length != 0){
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
                container6: playerdata.filter(item => !data["players"].includes(item)),
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
