import { Settings } from "lucide-react";

interface SettingsButtonProps {
  onClick?: () => void;
}

const SettingsButton = ({ onClick }: SettingsButtonProps) => {
  return (
    <button
      onClick={onClick}
      data-tip="Settings"
      className="btn tooltip absolute right-10 m-auto flex items-center justify-center rounded-full border-none bg-transparent p-3"
    >
      <Settings />
    </button>
  );
};

export default SettingsButton;
