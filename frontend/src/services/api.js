// for api calls to the backend

// npm install typescript @types/react @types/react-dom -for changing to typescript

import axios from "axios"

const API = "http://localhost:8000"

export const getNextRace = async () => {
    try {
        const response = await axios.get(`${API}/api/next-race`)
        return response.data
    } catch(error) {
        console.error("Error fetching data from api. See detailsL", error)
        throw error
    }
}

console.log(getNextRace())