"use client";
import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
  useMemo,
} from "react";
import { setApiToken, setLogoutCallback } from "@/lib/api";

interface AuthContextType {
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  loading: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load token from localStorage on initial mount
    const savedToken = localStorage.getItem("accessToken");
    if (savedToken) {
      setToken(savedToken);
      setApiToken(savedToken);
      // Also set it in cookies for middleware
      document.cookie = `auth_token=${savedToken}; path=/; max-age=${60 * 60 * 24 * 7}`; // 7 days
    }
    setLoading(false);
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem("accessToken", newToken);
    setToken(newToken);
    setApiToken(newToken);
    // Set cookie for middleware
    document.cookie = `auth_token=${newToken}; path=/; max-age=${60 * 60 * 24 * 7}`; // 7 days
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    setToken(null);
    setApiToken(null);
    // Clear cookie
    document.cookie = "auth_token=; path=/; max-age=0";
  };

  useEffect(() => {
    setLogoutCallback(logout);
  }, []);

  const value = useMemo(
    () => ({ token, login, logout, loading }),
    [token, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}