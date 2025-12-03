export interface User {
  id: number;
  email: string;
  name?: string;
  role?: "user" | "admin";
}

export interface LoginInput {
  email: string;
  password: string;
}

export interface LoginOutput {
  token: string;
  user: User;
}

export interface SignupInput {
  email: string;
  password: string;
  name?: string;
}

export interface AuthContextType {
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  signup?: (email: string, password: string) => Promise<void>; // added
  loading: boolean;
}

