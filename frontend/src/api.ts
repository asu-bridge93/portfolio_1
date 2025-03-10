import axios from "axios";

const API_URL = "http://localhost:8000"; // FastAPIサーバーのURL

export const predictIris = async (data: number[]) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, { features: data });
    return response.data;
  } catch (error) {
    console.error("Prediction error:", error);
    throw error;
  }
};
