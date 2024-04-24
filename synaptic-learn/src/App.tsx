import { RouterProvider, createBrowserRouter } from "react-router-dom";

import HomePage from "@/pages/home";
import PlotsPage from "@/pages/plots";
import ModalProvider from "@/providers/modal-provider";

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
  return (
    <>
      <ModalProvider />
      <RouterProvider router={router} />;
    </>
  );
}

export default App;
