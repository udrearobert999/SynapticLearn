import { RouterProvider, createBrowserRouter } from "react-router-dom";

import HomePage from "@/pages/home";
import PlotsPage from "@/pages/plots";

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
  return <RouterProvider router={router} />;
}

export default App;
