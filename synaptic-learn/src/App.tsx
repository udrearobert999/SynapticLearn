import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import HomePage from "@/pages/home";
import PlotsPage from "@/pages/plots";
import ModalProvider from "@/providers/modal-provider";
import { useSettingsStore } from "@/hooks/use-settings-store";
import { useEffect } from "react";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/plots",
    element: <PlotsPage />,
  },
]);

// Create a QueryClient instance
const queryClient = new QueryClient();

function App() {
  const { theme } = useSettingsStore();

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <QueryClientProvider client={queryClient}>
      <ModalProvider />
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}

export default App;
