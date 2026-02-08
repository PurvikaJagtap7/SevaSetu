"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import AdminNavbar from "../components/AdminNavbar";
import Footer from "../components/Footer";
import {
  PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis,
  LineChart, Line
} from "recharts";

export default function DashboardPage() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
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

      const response = await fetch(`http://localhost:5000/api/dashboard/stats/${adminId}`);
      const result = await response.json();
      
      if (result.status === "success") {
        setDashboardData(result.stats);
      } else {
        setError("Failed to load dashboard data");
      }
    } catch (err) {
      console.error("Error fetching dashboard:", err);
      setError("Failed to connect to server. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-blue-900 font-semibold">Loading dashboard...</p>
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

  const priorityData = dashboardData?.priorityData || [];
  const deptData = dashboardData?.deptData || [];
  const trendData = dashboardData?.trendData || [];
  const grievances = dashboardData?.grievances || [];
  const department = dashboardData?.department || "All Departments";
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <AdminNavbar />

      <div className="max-w-7xl mx-auto px-6 py-8 flex-1">

        <h1 className="text-2xl font-bold text-blue-900 mb-6">
          Admin Dashboard - {department}
        </h1>

        {/* Charts */}
        <div className="grid md:grid-cols-3 gap-6 mb-10">

          <ChartCard title="Priority Distribution">
            {priorityData.length > 0 ? (
              <PieChart width={220} height={220}>
                <Pie data={priorityData} dataKey="value" outerRadius={80} label>
                  <Cell fill="#dc2626" />
                  <Cell fill="#eab308" />
                  <Cell fill="#16a34a" />
                </Pie>
                <Tooltip />
              </PieChart>
            ) : (
              <p className="text-gray-500 text-sm py-8">No data available</p>
            )}
          </ChartCard>

          <ChartCard title="By Department">
            {deptData.length > 0 ? (
              <BarChart width={260} height={220} data={deptData}>
                <XAxis dataKey="dept" stroke="#1e3a8a" />
                <YAxis stroke="#1e3a8a" />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" radius={[6,6,0,0]} />
              </BarChart>
            ) : (
              <p className="text-gray-500 text-sm py-8">No data available</p>
            )}
          </ChartCard>

          <ChartCard title="Daily Trend (Last 7 Days)">
            {trendData.length > 0 ? (
              <LineChart width={260} height={220} data={trendData}>
                <XAxis dataKey="day" stroke="#1e3a8a" />
                <YAxis stroke="#1e3a8a" />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="count"
                  stroke="#1e3a8a"
                  strokeWidth={3}
                  dot={{ r: 5 }}
                />
              </LineChart>
            ) : (
              <p className="text-gray-500 text-sm py-8">No data available</p>
            )}
          </ChartCard>

        </div>

        {/* Grievance Cards */}
        <h2 className="text-lg font-semibold text-blue-900 mb-4">
          Recent Grievance Records
        </h2>

        {grievances.length === 0 ? (
          <div className="bg-white shadow border p-8 rounded text-center">
            <p className="text-gray-500">No grievances found for your department</p>
          </div>
        ) : (
          <div className="space-y-4">
            {grievances.map((g, i) => (
              <div key={i} className="bg-white shadow border p-5 rounded flex justify-between items-center">

                <div>
                  <p className="font-bold text-blue-900 text-sm">{g.id}</p>
                  <p className="text-sm text-gray-700">{g.user} • {g.dept}</p>
                  <p className="text-xs text-gray-500">Submitted on {g.date}</p>
                </div>

                <div className="flex items-center gap-6">

                  <span className={`px-3 py-1 text-white text-xs rounded
                    ${g.priority === "High" ? "bg-red-600" :
                      g.priority === "Medium" ? "bg-yellow-500" :
                      "bg-green-600"}`}>
                    {g.priority}
                  </span>

                  <span className={`px-3 py-1 text-white text-xs rounded
                    ${g.status === "Resolved" ? "bg-green-600" : 
                     g.status === "In Process" ? "bg-blue-600" :
                     g.status === "Under Review" ? "bg-yellow-500" :
                     "bg-gray-600"}`}>
                    {g.status}
                  </span>

                  <Link href={`/admin/grievance/${g.id}`}>
                    <button className="text-blue-900 font-semibold underline">
                      View
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

function ChartCard({ title, children }) {
  return (
    <div className="bg-white shadow rounded p-4 text-center">
      <p className="font-semibold text-blue-900 mb-3">{title}</p>
      {children}
    </div>
  );
}
