// pages/years/[year]/page.js
// app/years/[year]/page.js
"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "../../../services/api";
import Navbar from "../../../components/Navbar";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function YearStatsPage() {
  const params = useParams();
  const router = useRouter();
  const year = params.year;

  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [countries, setCountries] = useState([]);
  const [selectedYear, setSelectedYear] = useState(year);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.getYearStats(year);
        setStats(res);
      } catch (err) {
        setError("Failed to load yearly stats");
      }
    };

    if (year) fetchStats();
  }, [year]);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const res = await api.getCountries();
        setCountries(res);
      } catch (err) {
        console.error("Failed to load country names");
      }
    };

    fetchCountries();
  }, []);

  const teamName = (id) => {
    const team = countries.find((c) => c.id === id);
    return team ? team.name : `Team ${id}`;
  };

  const handleYearChange = (e) => {
    const y = e.target.value;
    setSelectedYear(y);
    router.push(`/years/${y}`);
  };

  const chartData = stats?.top_teams.map(([id, score]) => ({
    name: teamName(id),
    goals: score,
  }));

  if (error) return <div>Error: {error}</div>;
  if (!stats) return <div>Loading stats for {year}...</div>;

  return (
    <div>
      <Navbar />
      <main style={{ padding: "1rem" }}>
        <h1>Yearly Stats: {year}</h1>

        <div style={{ marginBottom: "1rem" }}>
          <label>Select Year: </label>
          <input
            type="number"
            value={selectedYear}
            onChange={handleYearChange}
            style={{ marginLeft: "0.5rem" }}
          />
        </div>

        <h2>Top Scoring Teams</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 40, right: 20, top: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="name" type="category" />
            <Tooltip />
            <Bar dataKey="goals" fill="#3182CE" />
          </BarChart>
        </ResponsiveContainer>

        <h2>Match List</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Home</th>
              <th>Away</th>
              <th>Score</th>
              <th>Tournament</th>
            </tr>
          </thead>
          <tbody>
            {stats.matches.map((m, idx) => (
              <tr key={idx}>
                <td>{new Date(m.date).toLocaleDateString()}</td>
                <td>{m.home}</td>
                <td>{m.away}</td>
                <td>{m.score}</td>
                <td>{m.tournament}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}
