"use client";

import { useEffect, useState } from "react";
import api from "../../services/api";
import Navbar from "../../components/Navbar";

export default function PlayersPage() {
  const [players, setPlayers] = useState([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState("");
  const [score, setScore] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const data = await api.getAllPlayers(); // must return list of players with id+name
        setPlayers(data);
        if (data.length > 0) setSelectedPlayerId(data[0].id);
      } catch (err) {
        setError("Failed to load players");
      }
    };
    fetchPlayers();
  }, []);

  const fetchScore = async () => {
    try {
      const data = await api.getPlayer(selectedPlayerId);
      setScore(data.total_goals || 0); // adjust field name as needed
    } catch (err) {
      setError("Failed to fetch player score");
    }
  };

  return (
    <div>
      <Navbar />
      <main style={{ padding: "2rem" }}>
        <h1>Check Player Score</h1>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <label>Select Player:</label>
          <select
            value={selectedPlayerId}
            onChange={(e) => setSelectedPlayerId(e.target.value)}
          >
            {players.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>

          <button onClick={fetchScore}>Show Score</button>
        </div>

        {score !== null && (
          <div style={{ marginTop: "1rem" }}>
            <h2>Goals Scored: {score}</h2>
          </div>
        )}
      </main>
    </div>
  );
}
