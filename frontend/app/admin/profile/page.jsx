"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import AdminNavbar from "../../components/AdminNavbar";
import Footer from "../../components/Footer";

export default function AdminProfilePage() {
  const [admin, setAdmin] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAdminProfile();
  }, []);

  const fetchAdminProfile = async () => {
    try {
      // Get admin info from sessionStorage
      const userData = sessionStorage.getItem("user");
      if (!userData) {
        setError("Not logged in");
        setLoading(false);
        return;
      }

      const user = JSON.parse(userData);
      const adminId = user.id;

      const response = await axios.get(`http://localhost:5000/api/admin/profile/${adminId}`);
      
      if (response.data.status === "success") {
        setAdmin(response.data.profile);
      } else {
        setError("Failed to load profile");
      }
    } catch (err) {
      console.error("Error fetching profile:", err);
      setError("Failed to connect to server. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-blue-900 font-semibold">Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex flex-col">
        <AdminNavbar />
        <div className="flex items-center justify-center flex-1">
          <div className="bg-red-50 border border-red-200 p-6 rounded">
            <p className="text-red-600 font-semibold">⚠️ {error}</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (!admin) return null;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <AdminNavbar />

      <div className="flex justify-center px-4 mt-10 flex-1">
        <div className="bg-white w-full max-w-3xl border shadow-md p-8 rounded">

          <h2 className="text-2xl font-bold text-blue-900 mb-6 border-b pb-3">
            Admin Profile
          </h2>

          <div className="grid md:grid-cols-2 gap-8 text-sm">

            <ProfileItem label="Officer Name" value={admin.name} />
            <ProfileItem label="Department" value={admin.department} />
            <ProfileItem label="Position" value={admin.position} />
            <ProfileItem label="Government Under" value={admin.governmentUnder} />
            <ProfileItem label="Official Email" value={admin.email} />
            <ProfileItem
              label="Total Grievances Handled"
              value={admin.totalHandled}
            />
            <ProfileItem
              label="Resolved Grievances"
              value={admin.resolved}
            />
            <ProfileItem
              label="Pending Grievances"
              value={admin.pending}
            />

          </div>

        </div>
      </div>

      <Footer />
    </div>
  );
}

function ProfileItem({ label, value }) {
  return (
    <div>
      <p className="text-gray-500 mb-1">{label}</p>
      <p className="font-semibold text-gray-900">
        {value || "—"}
      </p>
    </div>
  );
}
