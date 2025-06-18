import React, { useState, useMemo } from "react";

export default function MatchTable({ matches }) {
  const [sortBy, setSortBy] = useState("date");
  const [filterTeam, setFilterTeam] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const filteredMatches = useMemo(() => {
    let result = [...matches];

    if (filterTeam.trim()) {
      const term = filterTeam.toLowerCase();
      result = result.filter(
        (m) =>
          m.home_team.toLowerCase().includes(term) ||
          m.away_team.toLowerCase().includes(term)
      );
    }

    if (sortBy === "score") {
      result.sort(
        (a, b) =>
          b.home_score + b.away_score - (a.home_score + a.away_score)
      );
    } else {
      result.sort(
        (a, b) => new Date(b.match_date) - new Date(a.match_date)
      );
    }

    return result;
  }, [matches, sortBy, filterTeam]);

  const totalPages = Math.ceil(filteredMatches.length / itemsPerPage);
  const paginatedMatches = filteredMatches.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return isNaN(d) ? dateStr : d.toLocaleDateString();
  };

  return (
    <div style={{ color: "#f5f5f5" }}>
      <div style={{ marginBottom: "1rem", display: "flex", gap: "1rem" }}>
        <input
          type="text"
          placeholder="Filter by team name..."
          value={filterTeam}
          onChange={(e) => setFilterTeam(e.target.value)}
          style={{
            padding: "0.5rem",
            borderRadius: "4px",
            border: "1px solid #555",
            backgroundColor: "#1e1e1e",
            color: "#f5f5f5",
          }}
        />
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          style={{
            padding: "0.5rem",
            borderRadius: "4px",
            backgroundColor: "#1e1e1e",
            color: "#f5f5f5",
            border: "1px solid #555",
          }}
        >
          <option value="date">Sort by Date</option>
          <option value="score">Sort by Score</option>
        </select>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={thStyle}>Date</th>
            <th style={thStyle}>Home Team</th>
            <th style={thStyle}>Away Team</th>
            <th style={thStyle}>Score</th>
            <th style={thStyle}>Tournament</th>
          </tr>
        </thead>
        <tbody>
          {paginatedMatches.map((match, index) => (
            <tr key={index}>
              <td style={tdStyle}>{formatDate(match.match_date)}</td>
              <td style={tdStyle}>{match.home_team}</td>
              <td style={tdStyle}>{match.away_team}</td>
              <td style={tdStyle}>
                {match.home_score} - {match.away_score}
              </td>
              <td style={tdStyle}>{match.tournament}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: "1rem", textAlign: "center" }}>
        <button
          onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          disabled={currentPage === 1}
          style={buttonStyle}
        >
          Previous
        </button>
        <span style={{ margin: "0 1rem" }}>
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
          disabled={currentPage === totalPages}
          style={buttonStyle}
        >
          Next
        </button>
      </div>
    </div>
  );
}

const thStyle = {
  border: "1px solid #444",
  padding: "8px",
  textAlign: "left",
  backgroundColor: "#1e1e1e",
  color: "#ccc",
};

const tdStyle = {
  border: "1px solid #333",
  padding: "8px",
  backgroundColor: "#181818",
};

const buttonStyle = {
  padding: "0.4rem 0.8rem",
  backgroundColor: "#333",
  color: "#f5f5f5",
  border: "1px solid #666",
  borderRadius: "4px",
  cursor: "pointer",
};
