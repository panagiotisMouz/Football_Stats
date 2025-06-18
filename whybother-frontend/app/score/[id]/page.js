// pages/score/[id]/page.js
"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Navbar from "../../../components/Navbar";
import CustomLineChart from "../../../components/LineChart";

export default function ScorerProfile() {
  const { id } = useParams();
  const [profile, setProfile] = useState(null);
  const [view, setView] = useState("both");
  const [error, setError] = useState(null);

 useEffect(() => {
  const fetchProfile = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/scorers/${id}`
      );
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      setProfile(data);
    } catch (err) {
      console.error("Error fetching scorer profile:", err);
      setError("Could not load scorer data.");
    }
  };

  if (id) fetchProfile();
}, [id]);


  if (error) return <div style={{ color: "red" }}>❌ {error}</div>;
  if (!profile) return <div>🔄 Loading scorer profile...</div>;

  const viewMap = {
    player_goals: ["player_goals"],
    team_goals_per_match: ["team_goals_per_match"],
    both: ["player_goals", "team_goals_per_match"],
  };

  return (
    <div>
      <Navbar />
      <main style={{ padding: "1rem" }}>
        <h1>{profile.player} Profile</h1>

        <p><strong>Country:</strong> {profile.country}</p>
        {profile.active_years && (
          <p><strong>Active Years:</strong> {profile.active_years.from} - {profile.active_years.to}</p>
        )}
        <p><strong>Total Goals:</strong> {profile.total_goals}</p>
        <p><strong>Max Goals in a Match:</strong> {profile.max_goals_in_match}</p>
        {profile.team_goals_per_match_overall !== null && (
          <p><strong>Team Goals/Match Overall:</strong> {profile.team_goals_per_match_overall.toFixed(2)}</p>
        )}

        <h2>Yearly Performance</h2>
        <label htmlFor="view">Select View: </label>
        <select
          id="view"
          value={view}
          onChange={(e) => setView(e.target.value)}
          style={{ marginBottom: "1rem" }}
        >
          <option value="both">Player + Team</option>
          <option value="player_goals">Only Player Goals</option>
          <option value="team_goals_per_match">Only Team Goals per Match</option>
        </select>

        {profile.yearly_stats && profile.yearly_stats.length > 0 ? (
          <CustomLineChart
            data={profile.yearly_stats}
            xKey="year"
            yKeys={viewMap[view]}
            labels={{
              player_goals: "Player Goals",
              team_goals_per_match: "Team Goals/Match",
            }}
          />
        ) : (
          <p>No yearly data available.</p>
        )}
      </main>
    </div>
  );
}
