"use client";

import Link from "next/link";
import { useState } from "react";

export default function LoginPage() {
  const [role, setRole] = useState("citizen");

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const validate = () => {
    let err = {};

    if (!form.username) err.username = "This field is required";
    if (!form.password) err.password = "Password is required";

    setErrors(err);
    return Object.keys(err).length === 0;
  };

  const handleLogin = () => {
    if (validate()) {
      alert(`${role.toUpperCase()} Login Validated (later → API call)`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">

      {/* Header */}
      <div className="bg-white shadow py-4 text-center">
        <h1 className="text-xl font-bold text-blue-900">Nyaya-Grievance</h1>
      </div>

      <div className="flex items-center justify-center flex-1 px-4">
        <div className="bg-white w-full max-w-md border shadow-md p-6">

          {/* Toggle Tabs */}
          <div className="flex mb-6 border rounded overflow-hidden">
            <button
              onClick={() => setRole("citizen")}
              className={`w-1/2 py-2 text-sm font-semibold transition
                ${role === "citizen"
                  ? "bg-blue-900 text-white"
                  : "bg-gray-100 text-gray-600"}`}
            >
              Citizen Login
            </button>

            <button
              onClick={() => setRole("admin")}
              className={`w-1/2 py-2 text-sm font-semibold transition
                ${role === "admin"
                  ? "bg-blue-900 text-white"
                  : "bg-gray-100 text-gray-600"}`}
            >
              Admin Login
            </button>
          </div>

          <h2 className="text-xl font-bold text-blue-900 mb-6 border-b pb-2">
            {role === "admin" ? "ADMIN LOGIN" : "USER LOGIN"}
          </h2>

          {/* Username */}
          <label className="block text-sm font-semibold mb-1">
            {role === "admin"
              ? "Officer ID / Email"
              : "Mobile No / Email Id"}
          </label>
          <input
            name="username"
            className="w-full border p-2 mb-1 text-sm"
            onChange={handleChange}
          />
          {errors.username && (
            <p className="text-red-600 text-xs mb-3">{errors.username}</p>
          )}

          {/* Password */}
          <label className="block text-sm font-semibold mb-1">Password</label>
          <input
            name="password"
            type="password"
            className="w-full border p-2 mb-1 text-sm"
            onChange={handleChange}
          />
          {errors.password && (
            <p className="text-red-600 text-xs mb-3">{errors.password}</p>
          )}

          {/* Login Button */}
          <button
            onClick={handleLogin}
            className="w-full bg-blue-900 text-white py-2 text-sm font-semibold mt-2"
          >
            LOGIN
          </button>

          {/* Signup only for citizen */}
          {role === "citizen" && (
            <Link href="/signup">
              <p className="text-center mt-4 text-blue-900 text-sm cursor-pointer underline">
                New User? Register Here
              </p>
            </Link>
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
