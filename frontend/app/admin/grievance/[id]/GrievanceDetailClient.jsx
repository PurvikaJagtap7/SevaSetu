"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import AdminNavbar from "@/app/components/AdminNavbar";
import Footer from "@/app/components/Footer";

export default function GrievanceDetailClient() {
  const params = useParams();
  const router = useRouter();
  const id = params.id;
  
  const [grievance, setGrievance] = useState(null);
  const [statusHistory, setStatusHistory] = useState([]);
  const [statusStages, setStatusStages] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState("");
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      fetchGrievance();
      fetchStatusHistory();
      fetchStatusStages();
    }
  }, [id]);

  const fetchGrievance = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/grievances/${id}`);
      
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.status === "success") {
        setGrievance(result.grievance);
        setSelectedStatus(result.grievance.status || "Pending");
        setError(null);
      } else {
        throw new Error(result.message || "Failed to load grievance");
      }
    } catch (error) {
      console.error("Error fetching grievance:", error);
      setError(error.message || "Failed to load grievance");
    } finally {
      setLoading(false);
    }
  };

  const fetchStatusHistory = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/grievances/${id}/history`);
      const result = await response.json();
      
      if (result.status === "success") {
        setStatusHistory(result.history);
      }
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  const fetchStatusStages = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/status-stages");
      const result = await response.json();
      
      if (result.status === "success") {
        setStatusStages(result.stages);
      }
    } catch (error) {
      console.error("Error fetching status stages:", error);
    }
  };

  const handleStatusUpdate = async () => {
    if (!selectedStatus) {
      alert("Please select a status");
      return;
    }

    if (selectedStatus === grievance?.status) {
      alert("Status is already set to this value");
      return;
    }

    setUpdating(true);

    try {
      // Get admin info from sessionStorage
      const adminData = sessionStorage.getItem("user");
      let adminId = null;
      if (adminData) {
        try {
          const admin = JSON.parse(adminData);
          adminId = admin.id;
          console.log("✅ Admin ID:", adminId);
        } catch (e) {
          console.error("❌ Could not parse admin data:", e);
        }
      } else {
        console.warn("⚠️ No admin data in sessionStorage");
      }

      const requestBody = {
        status: selectedStatus,
        note: note,
        admin_id: adminId,
      };

      console.log("📤 Sending status update:", requestBody);
      console.log("📍 URL:", `http://localhost:5000/api/grievances/${id}/status`);

      const response = await fetch(`http://localhost:5000/api/grievances/${id}/status`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      console.log("📥 Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Server error:", errorText);
        throw new Error(`Server returned ${response.status}: ${errorText}`);
      }

      const result = await response.json();
      console.log("✅ Result:", result);

      if (result.status === "success") {
        alert(`✅ Status updated successfully!\n\n${result.whatsapp_sent ? "📱 WhatsApp notification sent." : result.whatsapp_error ? "⚠️ WhatsApp failed: " + result.whatsapp_error : ""}`);
        setNote("");
        await fetchGrievance();
        await fetchStatusHistory();
      } else {
        alert(`❌ Failed to update status\n\n${result.message || "Unknown error"}`);
      }
    } catch (error) {
      console.error("❌ Error updating status:", error);
      alert(`❌ Failed to update status\n\nError: ${error.message}\n\nPlease check:\n1. Flask server is running on port 5000\n2. Grievance ID is correct\n3. Check browser console for details`);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <AdminNavbar />
        <div className="flex items-center justify-center flex-1">
          <div className="text-center">
            <p className="text-blue-900 font-semibold text-lg mb-2">Loading grievance details...</p>
            <p className="text-gray-500 text-sm">Please wait</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !grievance) {
    return (
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <AdminNavbar />
        <div className="flex items-center justify-center flex-1">
          <div className="bg-red-50 border border-red-200 p-6 rounded max-w-md">
            <p className="text-red-600 font-semibold mb-4">⚠️ {error || "Grievance not found"}</p>
            <button
              onClick={() => router.push("/dashboard")}
              className="bg-blue-900 text-white px-4 py-2 rounded hover:bg-blue-800"
            >
              Back to Dashboard
            </button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

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

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <AdminNavbar />

      <div className="max-w-6xl mx-auto px-6 py-8 flex-1">
        <div className="mb-6">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-blue-900 hover:underline mb-2 flex items-center gap-1"
          >
            ← Back to Dashboard
          </button>
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
            <Detail label="Citizen Name" value={grievance.user_name || "Guest"} />
            <Detail label="Phone" value={grievance.user_phone} />
            <Detail label="Email" value={grievance.user_email || "N/A"} />
            <Detail label="Department" value={grievance.department} />
            <Detail label="Priority" value={grievance.priority} />
            
            <div>
              <p className="text-sm font-semibold text-gray-600 mb-1">Status</p>
              <span className={`px-3 py-1 text-white text-sm rounded ${getStatusColor(grievance.status)}`}>
                {grievance.status}
              </span>
            </div>

            <Detail label="Submitted On" value={new Date(grievance.created_at).toLocaleDateString()} />
            <Detail label="Last Updated" value={new Date(grievance.updated_at).toLocaleDateString()} />

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

          {/* RIGHT SIDE — STATUS UPDATE */}
          <div className="bg-white shadow rounded p-6 space-y-4">
            <h2 className="text-xl font-bold text-blue-900 mb-4">
              Update Status
            </h2>

            <div>
              <label className="block text-sm font-semibold mb-2">
                Current Status: <span className={`px-2 py-1 text-white text-xs rounded ${getStatusColor(grievance.status)}`}>{grievance.status}</span>
              </label>
            </div>

            <div>
              <label className="block text-sm font-semibold mb-2">
                New Status *
              </label>
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="w-full border p-3 rounded text-sm"
                disabled={updating}
              >
                {statusStages.map((stage) => (
                  <option key={stage} value={stage}>
                    {stage}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold mb-2">
                Update Note (Optional)
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Add a note about this status update..."
                className="w-full border p-3 rounded text-black placeholder-gray-400 text-sm"
                rows={4}
                disabled={updating}
              />
            </div>

            <button
              onClick={handleStatusUpdate}
              disabled={updating || selectedStatus === grievance.status}
              className="w-full bg-blue-900 text-white px-4 py-2 rounded disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {updating ? "Updating..." : "Update Status"}
            </button>

            {/* Status History */}
            {statusHistory.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-3">
                  Status History
                </h3>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {statusHistory.map((entry, idx) => (
                    <div key={idx} className="bg-gray-50 border p-3 rounded text-sm">
                      <div className="flex justify-between items-start mb-1">
                        <span className={`px-2 py-1 text-white text-xs rounded ${getStatusColor(entry.new_status)}`}>
                          {entry.new_status}
                        </span>
                        <span className="text-gray-500 text-xs">
                          {new Date(entry.created_at).toLocaleString()}
                        </span>
                      </div>
                      {entry.old_status && (
                        <p className="text-xs text-gray-600 mb-1">
                          Changed from: {entry.old_status}
                        </p>
                      )}
                      {entry.note && (
                        <p className="text-xs text-gray-700 mt-1">
                          Note: {entry.note}
                        </p>
                      )}
                      {entry.admin_name && (
                        <p className="text-xs text-gray-500 mt-1">
                          Updated by: {entry.admin_name}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
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
