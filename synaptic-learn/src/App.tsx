import { RouterProvider, createBrowserRouter } from "react-router-dom";

import HomePage from "@/pages/home";
import PlotsPage from "@/pages/plots";
import ModalProvider from "@/providers/modal-provider";
import { useSettingsStore } from "./hooks/use-settings-store";
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

function App() {
  const { theme } = useSettingsStore();

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <>
      <ModalProvider />
      <RouterProvider router={router} />
    </>
  );
}

export default App;
