// app/global/page.js
"use client";

import { useEffect, useState } from "react";
import api from "../../services/api";
import Navbar from "../../components/Navbar";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ScatterChart,
  Scatter,
  ZAxis
} from "recharts";

export default function GlobalStatsPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.getGlobalStats();
        setStats(res);
      } catch (err) {
        setError("Failed to load global stats");
      }
    };

    fetchStats();
  }, []);

  if (error) return <div>Error: {error}</div>;
  if (!stats) return <div>Loading global stats...</div>;

  return (
    <div>
      <Navbar />
      <main style={{ padding: "1rem" }}>
        <h1>Global Statistics</h1>

        <h2>Top 10 Countries by Wins</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stats.top10_wins} layout="vertical" margin={{ left: 40, right: 20, top: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="country" type="category" />
            <Tooltip />
            <Bar dataKey="wins" fill="#3182CE" />
          </BarChart>
        </ResponsiveContainer>

        <h2>Top 10 Countries by Points</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stats.top10_points} layout="vertical" margin={{ left: 40, right: 20, top: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="country" type="category" />
            <Tooltip />
            <Bar dataKey="points" fill="#2B6CB0" />
          </BarChart>
        </ResponsiveContainer>

        <h2>Top 10 Countries by Goals</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stats.top10_goals} layout="vertical" margin={{ left: 40, right: 20, top: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="country" type="category" />
            <Tooltip />
            <Bar dataKey="goals" fill="#68D391" />
          </BarChart>
        </ResponsiveContainer>

        <h2>Wins vs Population (Scatter)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
            <CartesianGrid />
            <XAxis dataKey="population" name="Population" />
            <YAxis dataKey="wins" name="Wins" />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter name="Countries" data={stats.population_scatter} fill="#4299E1" />
          </ScatterChart>
        </ResponsiveContainer>

        <h2>Wins vs Area (Scatter)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ left: 20, right: 20, top: 10, bottom: 10 }}>
            <CartesianGrid />
            <XAxis dataKey="area_sq_km" name="Area (km²)" />
            <YAxis dataKey="wins" name="Wins" />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter name="Countries" data={stats.scatter_wins_area} fill="#48BB78" />
          </ScatterChart>
        </ResponsiveContainer>

        <h2>Top 10 Normalized Wins per Year</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stats.top10_normalized_wins} layout="vertical" margin={{ left: 40, right: 20, top: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="country" type="category" />
            <Tooltip />
            <Bar dataKey="wins_per_year" fill="#DD6B20" />
          </BarChart>
        </ResponsiveContainer>
      </main>
    </div>
  );
}
