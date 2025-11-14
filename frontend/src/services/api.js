import axios from "axios"

const BASE_URL = "http://localhost:8000" // Or wherever your FastAPI server is

export const getContacts = () => axios.get(`${BASE_URL}/chats`)
export const getChatMessages = (username, limit = 100) =>
  axios.get(`${BASE_URL}/chat/${username}/messages?limit=${limit}`)
export const getUserStyle = (username) =>
  axios.get(`${BASE_URL}/chat/${username}/style`)
export const runLLM = (payload) => axios.post(`${BASE_URL}/llm`, payload)
