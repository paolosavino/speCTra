import axios from 'axios';

// Create an instance with default config
const api = axios.create({
    baseURL: '/', // Proxied by Vite to localhost:8000
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the token if we had user auth (admin)
// For verify, we just use the keys. 
// But we need a way to manage keys. 
// If we implement an "Admin" token later, we add it here.

export default api;
