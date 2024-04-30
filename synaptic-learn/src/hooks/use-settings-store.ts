import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

interface SettingsStore {
  maxResults: number;
  theme: string;
  setMaxResults: (maxResults: number) => void;
  toggleTheme: () => void;
}

export const useSettingsStore = create(
  persist<SettingsStore>(
    (set, get) => ({
      maxResults: 3,
      theme: "light",

      setMaxResults: (maxResults: number) => {
        set({ maxResults });
      },

      toggleTheme: () => {
        const newTheme = get().theme === "light" ? "dark" : "light";
        set({ theme: newTheme });
      },
    }),
    {
      name: "settings-storage",
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
