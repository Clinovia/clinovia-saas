"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";

interface NavLink {
  label: string;
  href: string;
}

const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/#hero" },
  { label: "Modules", href: "/explore" },
  { label: "Cardiology", href: "/#cardiology" },
  { label: "Neurology", href: "/#neurology" },
  { label: "Related Papers", href: "/#papers" },
  { label: "Features", href: "/#features" },
];

export default function Navbar() {
  const { token, logout, loading } = useAuth();

  return (
    <header className="fixed top-0 left-0 w-full bg-white shadow-sm z-50">
      <div className="flex justify-between items-center px-10 py-4 max-w-7xl mx-auto">
        
        {/* Brand */}
        <div className="text-2xl font-bold text-[#1B4D3E]">
          <Link href="/" className="hover:underline transition-colors">
            Clinovia
          </Link>
        </div>

        <nav className="flex space-x-8 items-center">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-[#1B4D3E] font-normal hover:underline hover:text-green-700 transition-colors"
            >
              {link.label}
            </Link>
          ))}

          {/* Auth */}
          {loading ? (
            <div className="ml-4 text-gray-400">Loading...</div>
          ) : token ? (
            <Button onClick={logout} className="ml-4">
              Logout
            </Button>
          ) : (
            <Link href="/login">
              <Button className="ml-4">Sign In</Button>
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}
