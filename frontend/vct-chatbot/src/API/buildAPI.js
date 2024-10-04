import axios from 'axios';

async function buildTeam(user_input) {
    try {
        console.log(user_input); // Log for debugging; consider removing or using a logger in production

        // Send a POST request to the Flask API
        const response = await axios.post('http://localhost:5000/build_team', {
            parameters: user_input, // Ensure user_input is correctly structured
        });
        var string = "Here's your requested team: "
        for(const x of response.data){
            string = string + x + ", "
        }
        console.log(response)

        return string.substring(0, string.length - 2); // Return the response data for further processing
    } catch (error) {
        console.error('Error:', error);
        // Optionally, return an error message or handle it further
    }
};

export default buildTeam;
