"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const navItem = (href, label) => (
    <Link
      href={href}
      className={`px-3 py-1.5 rounded text-sm font-medium transition ${
        pathname === href
          ? "bg-blue-100 text-blue-900"
          : "text-blue-900 hover:bg-blue-50"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <div className="sticky top-0 bg-white shadow z-50">
      <div className="flex justify-between items-center px-6 h-16 max-w-7xl mx-auto">


        {/* Logo + Name */}
        <Link href="/" className="flex items-center">
  <div className="relative h-12 w-45"> 
    <Image
      src="/logo.jpeg"
      alt="Nyaya Grievance Logo"
      fill
      className="object-contain"
      priority
    />
  </div>
</Link>




        {/* Right Links */}
        <div className="flex gap-6 items-center">
          {navItem("/", "Home")}
          {navItem("/about", "About")}

          <Link href="/login">
            <button className="bg-blue-900 text-white px-4 py-1.5 rounded text-sm">
              Login
            </button>
          </Link>

          <Link href="/signup">
            <button className="border border-blue-900 text-blue-900 px-4 py-1.5 rounded text-sm">
              Signup
            </button>
          </Link>
        </div>

      </div>
    </div>
  );
}
