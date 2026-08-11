import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AuthTokens, User } from "@/types/auth";

interface AuthState {
  access: string | null;
  refresh: string | null;
  user: User | null;
  isHydrated: boolean;
  isAdmin: () => boolean;
  setAuth: (tokens: AuthTokens, user: User) => void;
  setTokens: (tokens: AuthTokens) => void;
  setUser: (user: User) => void;
  logout: () => void;
  setHydrated: () => void;
}

/**
 * Tokenlar localStorage'da saqlanadi (backend cookie o'rnatmaydi, sof JWT bearer).
 * skipHydration:true — server-tomonda localStorage yo'q, shuning uchun hydration
 * providers.tsx ichida useEffect orqali qo'lda ishga tushiriladi (isHydrated bilan).
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      access: null,
      refresh: null,
      user: null,
      isHydrated: false,
      isAdmin: () => {
        const role = get().user?.role;
        return role === "admin" || role === "superadmin";
      },
      setAuth: (tokens, user) =>
        set({ access: tokens.access, refresh: tokens.refresh, user }),
      setTokens: (tokens) =>
        set({ access: tokens.access, refresh: tokens.refresh }),
      setUser: (user) => set({ user }),
      logout: () => set({ access: null, refresh: null, user: null }),
      setHydrated: () => set({ isHydrated: true }),
    }),
    {
      name: "auth-storage",
      skipHydration: true,
      partialize: (state) => ({
        access: state.access,
        refresh: state.refresh,
        user: state.user,
      }),
    }
  )
);
