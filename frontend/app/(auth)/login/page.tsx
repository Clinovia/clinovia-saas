"use client";
import { useState, useEffect, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext"; // ✅ Add this
import { authApi } from "@/lib/api/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth(); // ✅ Get login from context
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  
  const emailInputRef = useRef<HTMLInputElement>(null);
  const passwordInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const emailParam = searchParams.get("email");
    if (emailParam) {
      // Basic email validation before pre-filling
      if (/^\S+@\S+\.\S+$/.test(emailParam)) {
        setEmail(emailParam);
        toast.info("Welcome back! Please enter your password.");
        // Auto-focus password field after email is pre-filled
        passwordInputRef.current?.focus();
      } else {
        // Invalid email in URL? Clear it and focus email field
        setEmail("");
        emailInputRef.current?.focus();
      }
    } else {
      // No pre-fill → focus email field
      emailInputRef.current?.focus();
    }
  }, [searchParams]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;

    setLoading(true);
    try {
      const response = await authApi.login({ email, password });
      toast.success("Login successful!");
      
      login(response.access_token); // ✅ Use context login - handles localStorage AND state
      
      router.push("/protected");
    } catch (err: any) {
      toast.error(err.message || "Login failed. Please check your credentials.");
      setPassword(""); // Clear password on error for security
      passwordInputRef.current?.focus();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-50">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle>Welcome Back</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                ref={emailInputRef}
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                disabled={loading}
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                ref={passwordInputRef}
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                disabled={loading}
              />
            </div>
            <Button className="w-full" type="submit" disabled={loading}>
              {loading ? "Logging in..." : "Log In"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}