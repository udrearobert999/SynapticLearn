import ModelPlot from "@/components/model-plot";
import SettingsButton from "@/components/settings-button";
import { useModal } from "@/hooks/use-modal-store";
import { MoveLeft } from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

const baseModelPlotUrl = "http://localhost:5000/base-model-plot";
const trainedModelPlotUrl = "http://localhost:5000/trained-model-plot";

const PlotsPage = () => {
  const { onOpen } = useModal();
  const [activeTab, setActiveTab] = useState<"base" | "trained">("base");

  return (
    <div className="relative flex h-[90vh] w-[100vw] flex-col items-center justify-center gap-2 overflow-hidden">
      <button className="btn btn-primary absolute left-20 top-14 w-44 rounded-full">
        <NavLink
          to="/"
          className="flex h-full w-full items-center justify-center gap-4"
        >
          <MoveLeft /> Go Back
        </NavLink>
      </button>
      <div role="tablist" className="tabs-boxed tabs w-[50%]">
        <a
          role="tab"
          className={`tab ${activeTab === "base" ? "tab-active" : ""}`}
          onClick={() => setActiveTab("base")}
        >
          Base Model Plot
        </a>
        <a
          role="tab"
          className={`tab ${activeTab === "trained" ? "tab-active" : ""}`}
          onClick={() => setActiveTab("trained")}
        >
          Trained Model Plot
        </a>
      </div>
      <div className="flex h-[55%] w-[70%]">
        {activeTab === "base" ? (
          <ModelPlot plotUrl={baseModelPlotUrl} />
        ) : (
          <ModelPlot plotUrl={trainedModelPlotUrl} />
        )}
      </div>
      <div className="fixed bottom-0 left-0 right-0 flex min-h-28 w-full items-center justify-center border-t-2 border-gray-600/20 bg-base-100">
        <SettingsButton onClick={() => onOpen("settings")} />
      </div>
    </div>
  );
};

export default PlotsPage;
