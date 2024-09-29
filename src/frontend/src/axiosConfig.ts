// src/axiosConfig.ts

import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8001', // Adjust to your FastAPI server URL
});

export default instance;
