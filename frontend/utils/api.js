import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // FastAPI default port
    headers: {
        'Content-Type': 'application/json',
    },
});

export const chatWithTodo = async (message) => {
    const response = await api.post('/chat', { message });
    return response.data;
};

export default api;
