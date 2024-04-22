import { Brain } from "lucide-react";

const AppTitle = () => {
  return (
    <div className="flex items-center space-x-4">
      <Brain size={60} className=" text-purple" />{" "}
      <span className="text-5xl font-medium">
        <span className="font-bold">SYNAPTIC</span> LEARN
      </span>
    </div>
  );
};

export default AppTitle;
