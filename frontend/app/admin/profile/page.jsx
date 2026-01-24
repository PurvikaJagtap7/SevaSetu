"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import AdminNavbar from "../../components/AdminNavbar";
import Footer from "../../components/Footer";

export default function AdminProfilePage() {
  const [admin, setAdmin] = useState(null);

  useEffect(() => {
    // Later this will work directly when backend is ready
    axios.get("/api/admin/profile")
      .then((res) => setAdmin(res.data))
      .catch(() => {
        // Temporary empty state (no hardcoding)
        setAdmin({});
      });
  }, []);

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
