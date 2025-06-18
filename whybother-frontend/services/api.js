
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const api = {
  getCountryProfile: async (id, fromYear, toYear) => {
    const params = {};
    if (fromYear) params.from_year = fromYear;
    if (toYear) params.to_year = toYear;
    const res = await axios.get(`${API_BASE_URL}/stats/country/${id}/profile`, { params });
    return res.data;
  },

  getCountries: async () => {
    const res = await axios.get(`${API_BASE_URL}/countries`);
    return res.data;
  },

  getCountry: async (id) => {
    const res = await axios.get(`${API_BASE_URL}/countries/${id}`);
    return res.data;
  },

  getCountryMatches: async (id) => {
    const res = await axios.get(`${API_BASE_URL}/countries/${id}/matches`);
    return res.data;
  },

  getYearStats: async (year) => {
    const res = await axios.get(`${API_BASE_URL}/stats/${year}`);
    return res.data;
  },

  getGlobalStats: async () => {
    const res = await axios.get(`${API_BASE_URL}/stats/global`);
    return res.data;
  },

  getAllPlayers: async () => {
    const res = await axios.get(`${API_BASE_URL}/players`);
    return res.data;
  },

  getPlayer: async (id) => {
    const res = await axios.get(`${API_BASE_URL}/players/${id}`);
    return res.data;
  }
};

export default api;
