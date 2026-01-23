"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function ReviewPage() {
  const router = useRouter();
  const [data, setData] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("grievanceData");
    if (stored) {
      setData(JSON.parse(stored));
    }
  }, []);

  if (!data) return null;

  const handleConfirm = () => {
    // Later → API call here
    setSubmitted(true);
    localStorage.removeItem("grievanceData");
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      {/* Header */}
      <div className="bg-white shadow py-4 text-center">
        <h1 className="text-xl font-bold text-blue-900">Nyaya-Grievance</h1>
      </div>

      <div className="flex justify-center px-4 mt-8 mb-12">
        <div className="bg-white w-full max-w-3xl border shadow-md p-8">

          <h2 className="text-2xl font-bold text-blue-900 mb-6 border-b pb-3">
            Confirm Your Complaint Details
          </h2>

          {/* ✅ Success Message */}
          {submitted && (
            <div className="bg-green-50 border border-green-300 text-green-800 p-4 mb-6 text-sm">
              Grievance submitted successfully. You can track it in the
              <span
                onClick={() => router.push("/track")}
                className="underline cursor-pointer font-semibold ml-1"
              >
                Track Grievances
              </span>{" "}
              section.
            </div>
          )}

          <Section title="Category (Hint Provided)">
            {data.category || "Not provided"}
          </Section>

          <Section title="Location / Address">
            {data.address}
          </Section>

          <Section title="Urgency Indicated">
            <span
              className={`px-3 py-1 rounded text-white text-sm
              ${
                data.urgency === "high"
                  ? "bg-red-600"
                  : data.urgency === "medium"
                  ? "bg-yellow-500"
                  : "bg-green-600"
              }`}
            >
              {data.urgency || "Not selected"}
            </span>
          </Section>

          <Section title="Grievance Description">
            {data.grievance}
          </Section>

          {data.image && (
            <Section title="Attached Image">
              <img
                src={URL.createObjectURL(data.image)}
                alt="uploaded"
                className="w-48 border mt-2"
              />
            </Section>
          )}

          {/* Buttons */}
          {!submitted && (
            <div className="flex flex-col md:flex-row gap-6 mt-10">
              <button
                onClick={() => router.back()}
                className="w-full border border-blue-900 text-blue-900 py-3 font-semibold"
              >
                Go Back & Edit
              </button>

              <button
                onClick={handleConfirm}
                className="w-full bg-blue-900 text-white py-3 font-semibold"
              >
                Confirm Submit
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="bg-blue-900 text-white text-center py-3 text-xs">
        © 2026 Nyaya-Grievance Portal
      </div>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="mb-6">
      <h3 className="text-sm font-semibold text-gray-600 mb-1">{title}</h3>
      <div className="text-base text-gray-900 bg-gray-50 p-3 border rounded">
        {children}
      </div>
    </div>
  );
}
