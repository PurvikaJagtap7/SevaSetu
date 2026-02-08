"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

export default function TrackGrievanceDetailPage() {
  const params = useParams();
  const id = params.id;
  
  const [grievance, setGrievance] = useState(null);
  const [statusHistory, setStatusHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      fetchGrievance();
      fetchStatusHistory();
    }
  }, [id]);

  const fetchGrievance = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/grievances/${id}`);
      const result = await response.json();
      
      if (result.status === "success") {
        setGrievance(result.grievance);
      } else {
        setError(result.message || "Grievance not found");
      }
    } catch (error) {
      console.error("Error fetching grievance:", error);
      setError("Failed to connect to server. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const fetchStatusHistory = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/grievances/${id}/history`);
      const result = await response.json();
      
      if (result.status === "success") {
        setStatusHistory(result.history || []);
      }
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "Pending":
        return "bg-gray-500";
      case "Under Review":
        return "bg-yellow-500";
      case "In Process":
        return "bg-blue-600";
      case "On Hold":
        return "bg-orange-500";
      case "Resolved":
        return "bg-green-600";
      case "Closed":
        return "bg-gray-700";
      default:
        return "bg-gray-500";
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    try {
      const date = new Date(dateString);
      return date.toLocaleString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-blue-900 font-semibold">Loading grievance details...</p>
      </div>
    );
  }

  if (error || !grievance) {
    return (
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <Navbar />
        <div className="flex items-center justify-center flex-1">
          <div className="bg-red-50 border border-red-200 p-6 rounded max-w-md">
            <p className="text-red-600 font-semibold mb-4">⚠️ {error || "Grievance not found"}</p>
            <Link href="/track">
              <button className="bg-blue-900 text-white px-4 py-2 rounded hover:bg-blue-800">
                Back to My Grievances
              </button>
            </Link>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Navbar />

      <div className="max-w-6xl mx-auto px-6 py-8 flex-1">
        <div className="mb-6">
          <Link href="/track">
            <button className="text-blue-900 hover:underline mb-4">← Back to My Grievances</button>
          </Link>
          <h1 className="text-2xl font-bold text-blue-900">
            Grievance Details
          </h1>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* LEFT SIDE — DETAILS */}
          <div className="bg-white shadow rounded p-6 space-y-4">
            <h2 className="text-xl font-bold text-blue-900 mb-4">
              Grievance Information
            </h2>

            <Detail label="Grievance ID" value={grievance.grievance_id} />
            <Detail label="Department" value={grievance.department} />
            <Detail label="Priority" value={grievance.priority} />
            
            <div>
              <p className="text-sm font-semibold text-gray-600 mb-1">Current Status</p>
              <span className={`px-3 py-1 text-white text-sm rounded ${getStatusColor(grievance.status)}`}>
                {grievance.status}
              </span>
            </div>

            <Detail label="Submitted On" value={formatDate(grievance.created_at)} />
            <Detail label="Last Updated" value={formatDate(grievance.updated_at)} />

            {grievance.city && grievance.state && (
              <Detail 
                label="Location" 
                value={`${grievance.area ? grievance.area + ", " : ""}${grievance.place ? grievance.place + ", " : ""}${grievance.city}, ${grievance.state}`} 
              />
            )}

            <div>
              <p className="text-sm font-semibold text-gray-600 mb-1">
                Grievance Description
              </p>
              <div className="bg-gray-50 border p-3 text-black rounded text-sm">
                {grievance.grievance_text}
              </div>
            </div>

            {grievance.structured_text && (
              <div>
                <p className="text-sm font-semibold text-gray-600 mb-1">
                  Structured Summary
                </p>
                <div className="bg-gray-50 border p-3 text-black rounded text-sm whitespace-pre-wrap">
                  {grievance.structured_text}
                </div>
              </div>
            )}

            {grievance.resolution_note && (
              <div>
                <p className="text-sm font-semibold text-gray-600 mb-1">
                  Resolution Note
                </p>
                <div className="bg-green-50 border border-green-200 p-3 text-black rounded text-sm">
                  {grievance.resolution_note}
                </div>
              </div>
            )}
          </div>

          {/* RIGHT SIDE — STATUS HISTORY */}
          <div className="bg-white shadow rounded p-6 space-y-4">
            <h2 className="text-xl font-bold text-blue-900 mb-4">
              Status History
            </h2>

            {statusHistory.length === 0 ? (
              <p className="text-gray-500 text-sm">No status history available</p>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {statusHistory.map((entry, idx) => (
                  <div key={idx} className="bg-gray-50 border p-4 rounded text-sm">
                    <div className="flex justify-between items-start mb-2">
                      <span className={`px-2 py-1 text-white text-xs rounded ${getStatusColor(entry.new_status)}`}>
                        {entry.new_status}
                      </span>
                      <span className="text-gray-500 text-xs">
                        {formatDate(entry.created_at)}
                      </span>
                    </div>
                    {entry.old_status && (
                      <p className="text-xs text-gray-600 mb-1">
                        Changed from: <span className="font-semibold">{entry.old_status}</span>
                      </p>
                    )}
                    {entry.note && (
                      <p className="text-xs text-gray-700 mt-2 p-2 bg-white rounded">
                        <span className="font-semibold">Note:</span> {entry.note}
                      </p>
                    )}
                    {entry.admin_name && (
                      <p className="text-xs text-gray-500 mt-2">
                        Updated by: {entry.admin_name}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}

function Detail({ label, value }) {
  return (
    <div>
      <p className="text-sm font-semibold text-gray-600">{label}</p>
      <p className="text-black">{value || "N/A"}</p>
    </div>
  );
}

