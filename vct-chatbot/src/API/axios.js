import axios from 'axios';

const buildTeam = async () => {
    try {
        const response = await axios.post('http://localhost:5000/build_team', {
            parameters: {
                na_players: 3,
                international_players: 2,
                strategy: 'hybrid offensive and defensive',
            },
        });

        console.log(response.data); // Handle the response data as needed
    } catch (error) {
        console.error('Error:', error);
    }
};
