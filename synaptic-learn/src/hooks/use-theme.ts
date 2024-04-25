import { useEffect, useState } from "react";

export const useTheme = () => {
  const getInitialTheme = () => {
    return localStorage.getItem("theme") || "light";
  };

  const [theme, setTheme] = useState(getInitialTheme());

  useEffect(() => {
    localStorage.setItem("theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return { theme, toggleTheme };
};
