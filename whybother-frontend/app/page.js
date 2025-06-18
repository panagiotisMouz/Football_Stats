
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "../services/api";
import Navbar from "../components/Navbar";

export default function HomePage() {
  const router = useRouter();
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [fromYear, setFromYear] = useState(1950);
  const [toYear, setToYear] = useState(2022);
  const [yearInput, setYearInput] = useState(2022);
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState("");
  const [playerGoals, setPlayerGoals] = useState(null);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const res = await api.getCountries();
        setCountries(res);
        if (res.length > 0) setSelectedCountry(res[0].id);
      } catch (err) {
        console.error("Failed to load countries", err);
      }
    };
    fetchCountries();
  }, []);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const res = await api.getAllPlayers();
        setPlayers(res);
        if (res.length > 0) setSelectedPlayer(res[0].id);
      } catch (err) {
        console.error("Failed to load players", err);
      }
    };
    fetchPlayers();
  }, []);

  const handleGoToCountry = () => {
    if (selectedCountry) {
      router.push(`/countries/${selectedCountry}?from_year=${fromYear}&to_year=${toYear}`);
    }
  };

  const handleGoToYear = () => {
    if (yearInput) {
      router.push(`/years/${yearInput}`);
    }
  };

  const handleCheckPlayer = async () => {
    try {
      router.push(`/score/${selectedPlayer}`);
    } catch (err) {
      console.error("Failed to go to player score page", err);
    }
  };

  return (
    <div>
      <Navbar />
      <main style={{ padding: "2rem" }}>
        <h1>Select Country Profile</h1>

        <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "2rem" }}>
          <label>Country:</label>
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
          >
            {countries.map((country) => (
              <option key={country.id} value={country.id}>
                {country.name}
              </option>
            ))}
          </select>

          <label>From:</label>
          <input
            type="number"
            value={fromYear}
            onChange={(e) => setFromYear(parseInt(e.target.value))}
          />

          <label>To:</label>
          <input
            type="number"
            value={toYear}
            onChange={(e) => setToYear(parseInt(e.target.value))}
          />

          <button onClick={handleGoToCountry} style={{ padding: "0.5rem 1rem" }}>
            View Profile
          </button>
        </div>

        <h2>Explore Other Stats</h2>
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <input
            type="number"
            value={yearInput}
            onChange={(e) => setYearInput(e.target.value)}
            placeholder="Enter year"
            style={{ width: "100px" }}
          />
          <button onClick={handleGoToYear} style={{ padding: "0.5rem 1rem" }}>Go to Year Stats</button>
          <button onClick={() => router.push("/global")} style={{ padding: "0.5rem 1rem" }}>Go to Global Stats</button>
        </div>

        <h2 style={{ marginTop: "2rem" }}>Check Player Goals</h2>
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <select value={selectedPlayer} onChange={(e) => setSelectedPlayer(e.target.value)}>
            {players.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
          <button onClick={handleCheckPlayer} style={{ padding: "0.5rem 1rem" }}>View Player Stats</button>
        </div>
      </main>
    </div>
  );
}
