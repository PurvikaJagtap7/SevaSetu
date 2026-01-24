"use client";

import Link from "next/link";
import Navbar from "../components/Navbar";

export default function TrackPage() {
  // Later from backend
  const grievances = [
    {
      id: "GRV-2026-00124",
      category: "Water & Sanitation",
      date: "23 Jan 2026",
      status: "In Progress",
    },
    {
      id: "GRV-2026-00110",
      category: "Infrastructure",
      date: "20 Jan 2026",
      status: "Resolved",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <Navbar />

      <div className="max-w-5xl mx-auto px-4 mt-10 flex-1">

        <h2 className="text-3xl font-bold text-blue-900 mb-2">
          Your Grievances
        </h2>
        <p className="text-gray-600 mb-8">
          Track the status and progress of all the complaints you have submitted.
        </p>

        <div className="space-y-6">
          {grievances.map((g, i) => (
            <div
              key={i}
              className="bg-white border shadow-md p-6 rounded-lg flex flex-col md:flex-row md:items-center md:justify-between gap-4 hover:shadow-lg transition"
            >
              {/* Left Info */}
              <div>
                <p className="text-lg font-bold text-blue-900">{g.id}</p>
                <p className="text-sm text-gray-600">{g.category}</p>
                <p className="text-xs text-gray-500">
                  Submitted on {g.date}
                </p>
              </div>

              {/* Status + Action */}
              <div className="flex items-center gap-6">
                <span
                  className={`px-4 py-1 text-sm text-white rounded-full
                  ${
                    g.status === "Resolved"
                      ? "bg-green-600"
                      : "bg-yellow-500"
                  }`}
                >
                  {g.status}
                </span>

                <button className="border border-blue-900 text-blue-900 px-4 py-1 text-sm rounded">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <Footer />
    </div>
  );
}


/* ---------- FOOTER ---------- */

function Footer() {
  return (
    <div className="bg-blue-900 text-white text-center py-3 text-xs mt-12">
      © 2026 Nyaya-Grievance Portal
    </div>
  );
}
