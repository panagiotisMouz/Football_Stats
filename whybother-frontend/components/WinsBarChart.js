// components/WinsBarChart.js
"use client";

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function WinsBarChart({ winsPerYear }) {
  if (!winsPerYear || winsPerYear.length === 0) return <p>No data available</p>;

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={winsPerYear}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="wins" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
