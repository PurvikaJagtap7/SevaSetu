"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function TrackPage() {
  const [grievances, setGrievances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGrievances();
  }, []);

  const fetchGrievances = async () => {
    try {
      // Get user ID from sessionStorage
      const userData = sessionStorage.getItem("user");
      if (!userData) {
        setError("Please login to view your grievances");
        setLoading(false);
        return;
      }

      const user = JSON.parse(userData);
      const userId = user.id;

      const response = await fetch(`http://localhost:5000/api/grievances/user/${userId}`);
      const result = await response.json();

      if (result.status === "success") {
        setGrievances(result.grievances || []);
      } else {
        setError(result.message || "Failed to load grievances");
      }
    } catch (err) {
      console.error("Error fetching grievances:", err);
      setError("Failed to connect to server. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "Resolved":
        return "bg-green-600";
      case "Closed":
        return "bg-gray-600";
      case "In Process":
        return "bg-blue-600";
      case "Under Review":
        return "bg-yellow-500";
      case "On Hold":
        return "bg-orange-500";
      default:
        return "bg-gray-500";
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-blue-900 font-semibold">Loading your grievances...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <Navbar />
        <div className="flex items-center justify-center flex-1">
          <div className="bg-red-50 border border-red-200 p-6 rounded">
            <p className="text-red-600 font-semibold">⚠️ {error}</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

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

        {grievances.length === 0 ? (
          <div className="bg-white border shadow-md p-8 rounded-lg text-center">
            <p className="text-gray-500 text-lg mb-2">No grievances found</p>
            <p className="text-gray-400 text-sm">Submit your first grievance to get started!</p>
            <Link href="/grievance">
              <button className="mt-4 bg-blue-900 text-white px-6 py-2 rounded hover:bg-blue-800">
                Submit Grievance
              </button>
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {grievances.map((g, i) => (
              <div
                key={i}
                className="bg-white border shadow-md p-6 rounded-lg flex flex-col md:flex-row md:items-center md:justify-between gap-4 hover:shadow-lg transition"
              >
                {/* Left Info */}
                <div>
                  <p className="text-lg font-bold text-blue-900">{g.grievance_id}</p>
                  <p className="text-sm text-gray-600">{g.department}</p>
                  <p className="text-xs text-gray-500">
                    Submitted on {formatDate(g.created_at)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Priority: <span className="font-semibold">{g.priority}</span>
                  </p>
                </div>

                {/* Status + Action */}
                <div className="flex items-center gap-6">
                  <span
                    className={`px-4 py-1 text-sm text-white rounded-full ${getStatusColor(g.status)}`}
                  >
                    {g.status}
                  </span>

                  <Link href={`/track/${g.grievance_id}`}>
                    <button className="border border-blue-900 text-blue-900 px-4 py-1 text-sm rounded hover:bg-blue-50">
                      View Details
                    </button>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
