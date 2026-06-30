import axios from "axios";

// In development, Vite proxies /api/* → http://127.0.0.1:8000/*
// This avoids CORS entirely in dev. In production, set VITE_API_URL.
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? "/api",
});

export default api;