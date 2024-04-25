import { useEffect, useState } from "react";

export const useMaxResults = () => {
  const getMaxResults = () => {
    return (localStorage.getItem("maxResults") || 3) as number;
  };

  const [maxResults, setMaxResults] = useState(getMaxResults());

  useEffect(() => {
    localStorage.setItem("maxResults", maxResults.toString());
  }, [maxResults]);

  return { maxResults, setMaxResults };
};
