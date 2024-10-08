import axios from 'axios';

async function buildTeam(user_input, setItems) {
    try {
        console.log(user_input); // Log for debugging; consider removing or using a logger in production

        // Send a POST request to the Flask API
        const response = await axios.post('http://localhost:5000/build_team', {
            parameters: user_input, // Ensure user_input is correctly structured
        });
        console.log(response.data)
        if (!Array.isArray(response.data)) {
          return response.data.content[0].text
        }
        var string = "Here's your requested team: "
        for(const x of response.data){
            string = string + x + ", "
        }
        setItems(prevItems => {
            // Get old items from container1 to container5
            const oldItems = [
              ...prevItems.container1,
              ...prevItems.container2,
              ...prevItems.container3,
              ...prevItems.container4,
              ...prevItems.container5,
            ];
          
            return {
              // Assign new values to container1 - container5
              container1: [response.data[0]],
              container2: [response.data[1]],
              container3: [response.data[2]],
              container4: [response.data[3]],
              container5: [response.data[4]], 
          
              // Add old items from container1 - container5 to container6, keeping previous values in container6
              container6: [...prevItems.container6.filter(item => !response.data.includes(item)), ...oldItems],
            };
          });
          
        console.log(response)

        return string.substring(0, string.length - 2); // Return the response data for further processing
    } catch (error) {
        console.error('Error:', error);
        throw error
    }
};

export default buildTeam;
