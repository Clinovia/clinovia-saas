import { LoginOutput } from "@/types/auth";

export type LoginResponse = LoginOutput | { error: string };

export async function login(email: string, password: string): Promise<LoginResponse> {
  try {
    const res = await fetch("/api/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      const errorData = await res.json();
      return { error: errorData.message || "Login failed" };
    }

    const data: LoginOutput = await res.json();
    return data;
  } catch (err) {
    return { error: "Network error" };
  }
}
