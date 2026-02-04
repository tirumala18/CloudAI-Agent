import axios from 'axios';

const API_BASE = 'http://localhost:8080'; // Replace with your controller URL

export const executeCommand = async (command) => {
  const res = await axios.post(`${API_BASE}/api/execute`, { command });
  return res.data;
};

