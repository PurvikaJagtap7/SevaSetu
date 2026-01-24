"use client";

import { useEffect, useState } from "react";
import AdminNavbar from "@/app/components/AdminNavbar";
import Footer from "@/app/components/Footer";

export default function GrievanceDetailClient({ id }) {
  const [grievance, setGrievance] = useState(null);
  const [note, setNote] = useState("");
  const [image, setImage] = useState(null);
  const [aiVerified, setAiVerified] = useState(false);

  /* -------- DUMMY DATA FOR UI -------- */

  useEffect(() => {
    const dummyGrievance = {
      id: id,
      citizenName: "Ramesh Kumar",
      department: "Water & Sanitation",
      priority: "High",
      status: "Open",
      date: "23 Jan 2026",
      description:
        "Water leakage near main road for last 5 days causing traffic and hygiene issues.",
    };

    setGrievance(dummyGrievance);
  }, [id]);

  /* -------- AI VERIFY (UI only) -------- */

  const handleAIVerify = () => {
    if (!note || !image) {
      alert("Resolution note and proof image required");
      return;
    }

    setAiVerified(true);
  };

  /* -------- CLOSE GRIEVANCE (UI only) -------- */

  const handleClose = () => {
    setGrievance({ ...grievance, status: "Resolved" });
  };

  if (!grievance) return null;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <AdminNavbar />

      <div className="max-w-6xl mx-auto px-6 py-8 flex-1 grid md:grid-cols-2 gap-8">

        {/* LEFT SIDE — DETAILS */}
        <div className="bg-white shadow rounded p-6 space-y-4">
          <h2 className="text-xl font-bold text-blue-900 mb-4">
            Grievance Information
          </h2>

          <Detail label="Grievance ID" value={grievance.id} />
          <Detail label="Citizen Name" value={grievance.citizenName} />
          <Detail label="Department" value={grievance.department} />
          <Detail label="Priority" value={grievance.priority} />
          <Detail label="Status" value={grievance.status} />
          <Detail label="Submitted On" value={grievance.date} />

          <div>
            <p className="text-sm font-semibold text-gray-600 mb-1">
              Grievance Description
            </p>
            <div className="bg-gray-50 border p-3 text-black rounded text-sm">
              {grievance.description}
            </div>
          </div>
        </div>

        {/* RIGHT SIDE — RESOLUTION */}
        <div className="bg-white shadow rounded p-6 space-y-4">
          <h2 className="text-xl font-bold text-blue-900 mb-4">
            Resolution & Proof
          </h2>

          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Write resolution notes..."
            className="w-full border p-3 rounded text-black placeholder-gray-400"
            rows={4}
          />

          <label className="flex flex-col items-center justify-center h-36 border-2 border-dashed border-blue-300 bg-blue-50 cursor-pointer">
            <p className="text-sm text-gray-700">
              Upload Proof Image (required)
            </p>
            <input
              type="file"
              onChange={(e) => setImage(e.target.files[0])}
              className="hidden"
            />
          </label>

          {image && (
            <p className="text-green-600 text-sm">
              ✓ {image.name} selected
            </p>
          )}

          <p className="text-sm text-gray-600">
            ⚠️ First, AI will verify that the uploaded proof and resolution
            notes genuinely solve the issue. Only after AI approval, you will be
            allowed to close the grievance.
          </p>

          {!aiVerified ? (
            <button
              onClick={handleAIVerify}
              className="bg-blue-900 text-white px-4 py-2 rounded"
            >
              Submit for AI Verification
            </button>
          ) : (
            <button
              onClick={handleClose}
              className="bg-green-600 text-white px-4 py-2 rounded"
            >
              Close Grievance
            </button>
          )}
        </div>

      </div>

      <Footer />
    </div>
  );
}

/* -------- REUSABLE -------- */

function Detail({ label, value }) {
  return (
    <div>
      <p className="text-sm font-semibold text-gray-600">{label}</p>
      <p className="text-black">{value}</p>
    </div>
  );
}
