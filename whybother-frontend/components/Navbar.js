"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav
      style={{
        padding: "1rem",
        backgroundColor: "#1e1e1e",
        color: "#f5f5f5",
        display: "flex",
        gap: "1.5rem",
        alignItems: "center",
        borderBottom: "1px solid #333",
      }}
    >
      <Link href="/" style={{ color: "#61dafb", textDecoration: "none" }}>
        Home
      </Link>
      <Link href="/global" style={{ color: "#61dafb", textDecoration: "none" }}>
        Global Stats
      </Link>
      <Link href="/score/1" style={{ color: "#61dafb", textDecoration: "none" }}>
        Scorer Example
      </Link>
      <Link href="/years/2022" style={{ color: "#61dafb", textDecoration: "none" }}>
        Year 2022
      </Link>
    </nav>
  );
}
