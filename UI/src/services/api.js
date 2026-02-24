import axios from 'axios';

const API_BASE = 'http://localhost:8080'; // Replace with your controller URL

export const executeCommand = async (command, accountId = null) => {
  try {
    const res = await axios.post(`${API_BASE}/api/execute`, { command, account_id: accountId }, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 900000, // 15 minute timeout (900 seconds)
    });
    return res.data;
  } catch (error) {
    // Provide detailed error information
    if (error.response) {
      // Backend returned an error response
      const detail = error.response.data?.detail || error.response.data?.message || 'Unknown error';
      throw new Error(`Backend Error (${error.response.status}): ${detail}`);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('No response from backend. Is the server running on http://localhost:8080?');
    } else {
      // Error in request setup
      throw new Error(`Request Error: ${error.message}`);
    }
  }
};

