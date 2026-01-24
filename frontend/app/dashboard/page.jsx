"use client";
import Link from "next/link";
import AdminNavbar from "../components/AdminNavbar";
import Footer from "../components/Footer";
import {
  PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis,
  LineChart, Line
} from "recharts";

/* ---------------- TEMP DATA (later from API) ---------------- */

const priorityData = [
  { name: "High", value: 12 },
  { name: "Medium", value: 18 },
  { name: "Low", value: 10 },
];

const deptData = [
  { dept: "Health", count: 22 },
  { dept: "Water", count: 35 },
  { dept: "Infra", count: 18 },
];

const trendData = [
  { day: "Mon", count: 5 },
  { day: "Tue", count: 8 },
  { day: "Wed", count: 6 },
  { day: "Thu", count: 10 },
];

const grievances = [
  {
    id: "GRV-00124",
    user: "Ramesh",
    dept: "Water",
    priority: "High",
    status: "In Progress",
    date: "23 Jan",
  },
  {
    id: "GRV-00110",
    user: "Sita",
    dept: "Infrastructure",
    priority: "Medium",
    status: "Resolved",
    date: "20 Jan",
  },
];

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      <AdminNavbar />

      <div className="max-w-7xl mx-auto px-6 py-8 flex-1">

        <h1 className="text-2xl font-bold text-blue-900 mb-6">
          Admin Dashboard Overview
        </h1>

        {/* Charts */}
        <div className="grid md:grid-cols-3 gap-6 mb-10">

          <ChartCard title="Priority Distribution">
            <PieChart width={220} height={220}>
              <Pie data={priorityData} dataKey="value" outerRadius={80} label>
                <Cell fill="#dc2626" />
                <Cell fill="#eab308" />
                <Cell fill="#16a34a" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ChartCard>

          <ChartCard title="By Department">
            <BarChart width={260} height={220} data={deptData}>
              <XAxis dataKey="dept" stroke="#1e3a8a" />
              <YAxis stroke="#1e3a8a" />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" radius={[6,6,0,0]} />
            </BarChart>
          </ChartCard>

          <ChartCard title="Daily Trend">
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
          </ChartCard>

        </div>

        {/* Grievance Cards */}
        <h2 className="text-lg font-semibold text-blue-900 mb-4">
          Grievance Records
        </h2>

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
                  ${g.status === "Resolved" ? "bg-green-600" : "bg-blue-600"}`}>
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
