import axios from "axios";
const API_BASE_URL = "http://localhost:8000/api/";
import { useAuth } from "../context/AuthContext";

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use(
  async (config) => {
    let accessToken = localStorage.getItem("access");
    const refreshToken = localStorage.getItem("refresh");

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem("refresh");

    // If access token expired, try refreshing it
    if (error.response?.status === 401 && refreshToken && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const response = await axios.post(`${API_BASE_URL}token/refresh/`, {
          refresh: refreshToken,
        });

        localStorage.setItem("access", response.data.access);
        api.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;
        return api(originalRequest); // Retry original request with new token
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        logoutUser(); // Clear tokens and logout user
      }
    }

    return Promise.reject(error);
  }
);

const logoutUser = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("username");
  window.location.href = "/login"; // Redirect to login
};

export default api;
