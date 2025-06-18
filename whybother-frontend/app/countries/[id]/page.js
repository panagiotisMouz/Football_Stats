"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "../../../services/api";
import Navbar from "../../../components/Navbar";
import WinsBarChart from "../../../components/WinsBarChart";

export default function CountryProfile() {
  const params = useParams();
  const id = params.id;

  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);
  const [fromYear, setFromYear] = useState(1950);
  const [toYear, setToYear] = useState(2022);

  const fetchProfile = async () => {
    try {
      const result = await api.getCountryProfile(id, fromYear, toYear);
      console.log("✅ API Result:", result);
      setProfile(result);
    } catch (err) {
      console.error("❌ Fetch error:", err);
      setError(err.message || "Error loading profile");
    }
  };

  useEffect(() => {
    if (id) fetchProfile();
  }, [id]);

  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>Loading country profile...</div>;

  return (
    <div>
      <Navbar />
      <main style={{ padding: "1rem" }}>
        <h1>{profile.country}</h1>
        <p>Region: {profile.region}</p>
        <p>Sub-region: {profile.sub_region || "N/A"}</p>
        <p>Population: {profile.population?.toLocaleString()}</p>
        <p>Area: {profile.area?.toLocaleString()} km²</p>

        <div style={{ marginTop: "1rem", marginBottom: "1rem" }}>
          <label>From Year: </label>
          <input
            type="number"
            value={fromYear}
            onChange={(e) => setFromYear(parseInt(e.target.value))}
          />
          <label style={{ marginLeft: "1rem" }}>To Year: </label>
          <input
            type="number"
            value={toYear}
            onChange={(e) => setToYear(parseInt(e.target.value))}
          />
          <button onClick={fetchProfile} style={{ marginLeft: "1rem" }}>
            Refresh
          </button>
        </div>

        <h2>Stats</h2>
        <ul>
          <li>Matches: {profile.stats?.matches}</li>
          <li>Wins: {profile.stats?.wins}</li>
          <li>Goals: {profile.stats?.goals}</li>
          <li>Points: {profile.stats?.points}</li>
          <li>Avg Goals: {profile.stats?.avg_goals}</li>
        </ul>

        <h2>Wins per Year</h2>
        <WinsBarChart winsPerYear={profile.wins_per_year || []} />

        <h2>Match History</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Opponent</th>
              <th>Venue</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(profile.matches) ? (
              profile.matches.map((match, idx) => (
                <tr key={idx}>
                  <td>{match.date}</td>
                  <td>{match.opponent}</td>
                  <td>{match.venue}</td>
                  <td>{match.score}</td>
                </tr>
              ))
            ) : (
              <tr><td colSpan="4">No match data available.</td></tr>
            )}
          </tbody>
        </table>
      </main>
    </div>
  );
}
