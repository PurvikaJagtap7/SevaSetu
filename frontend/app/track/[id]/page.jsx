"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Navbar from "@/app/components/Navbar";
import Footer from "@/app/components/Footer";

export default function GrievanceDetailsPage() {
  const { id } = useParams();
  const [grievance, setGrievance] = useState(null);

  /* ---------- DUMMY DATA FOR UI ---------- */
  useEffect(() => {
    const dummy = {
      id: id,
      category: "Water & Sanitation",
      address: "SV Road, Andheri West, Mumbai, Maharashtra",
      date: "23 Jan 2026",
      status: "In Progress",
      urgency: "High",
      description:
        "There is continuous water leakage from the main pipeline causing road damage and hygiene issues.",
      officerNote:
        "Team has inspected the site. Repair work scheduled within 2 days.",
    };

    setGrievance(dummy);
  }, [id]);

  if (!grievance) return null;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <Navbar />

      <div className="max-w-4xl mx-auto px-6 py-10 flex-1">

        <h2 className="text-3xl font-bold text-blue-900 mb-6">
          Grievance Details
        </h2>

        <div className="bg-white shadow border rounded-lg p-8 space-y-6">

          <Detail label="Grievance ID" value={grievance.id} />
          <Detail label="Category" value={grievance.category} />
          <Detail label="Location" value={grievance.address} />
          <Detail label="Submitted On" value={grievance.date} />

          <div>
            <p className="text-sm font-semibold text-gray-600 mb-1">Urgency</p>
            <span
              className={`px-3 py-1 text-white text-sm rounded-full
              ${
                grievance.urgency === "High"
                  ? "bg-red-600"
                  : grievance.urgency === "Medium"
                  ? "bg-yellow-500"
                  : "bg-green-600"
              }`}
            >
              {grievance.urgency}
            </span>
          </div>

          <div>
            <p className="text-sm font-semibold text-gray-600 mb-1">
              Your Description
            </p>
            <div className="bg-gray-50 border p-4 text-black rounded text-sm">
              {grievance.description}
            </div>
          </div>

          {/* Status Section */}
          <div className="border-t pt-6">
            <p className="text-sm font-semibold text-gray-600 mb-2">
              Current Status
            </p>

            <span
              className={`px-4 py-1 text-white text-sm rounded-full
              ${
                grievance.status === "Resolved"
                  ? "bg-green-600"
                  : "bg-yellow-500"
              }`}
            >
              {grievance.status}
            </span>
          </div>

        </div>
      </div>

      <Footer />
    </div>
  );
}

/* ---------- Reusable ---------- */

function Detail({ label, value }) {
  return (
    <div>
      <p className="text-sm font-semibold text-gray-600">{label}</p>
      <p className="text-black">{value}</p>
    </div>
  );
}
