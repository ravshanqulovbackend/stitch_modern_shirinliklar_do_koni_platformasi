import { http } from "../http";
import type {
  AuthTokens,
  ChangePasswordPayload,
  LoginPayload,
  RegisterPayload,
  RegisterResponse,
  User,
} from "@/types/auth";

export async function login(payload: LoginPayload): Promise<AuthTokens> {
  const { data } = await http.post<AuthTokens>("/users/login/", payload);
  return data;
}

export async function register(payload: RegisterPayload): Promise<RegisterResponse> {
  const { data } = await http.post<RegisterResponse>("/users/register/", payload);
  return data;
}

export async function fetchProfile(): Promise<User> {
  const { data } = await http.get<User>("/users/profile/");
  return data;
}

export async function updateProfile(payload: Partial<User>): Promise<User> {
  const { data } = await http.patch<User>("/users/profile/", payload);
  return data;
}

export async function changePassword(payload: ChangePasswordPayload): Promise<{ detail: string }> {
  const { data } = await http.post<{ detail: string }>("/users/change-password/", payload);
  return data;
}

export async function logoutRequest(refresh: string): Promise<void> {
  await http.post("/users/logout/", { refresh });
}
