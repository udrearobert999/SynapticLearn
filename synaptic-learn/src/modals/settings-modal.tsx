import { useModal } from "@/hooks/use-modal-store";
import { useSettingsStore } from "@/hooks/use-settings-store";
import { useQueryClient } from "@tanstack/react-query";
import { Moon, Sun, Trash2 } from "lucide-react";
import { ChangeEvent, useEffect } from "react";

const SettingsModal = () => {
  const { isOpen, type, onClose } = useModal();
  const { theme, toggleTheme, maxResults, setMaxResults } = useSettingsStore();
  const queryClient = useQueryClient();

  const isModalOpen = isOpen && type === "settings";
  useEffect(() => {
    const modal = document.getElementById("modal") as HTMLDialogElement | null;
    if (!modal) return;

    if (isModalOpen) modal.showModal();
    else {
      modal.close();
      onClose();
    }
  }, [isModalOpen, onClose]);

  const handleMaxResultsChange = (e: ChangeEvent<HTMLInputElement>) => {
    const sliderValue = Number(e.currentTarget.value);
    const newMaxResults = sliderValue / 25 + 1;
    setMaxResults(newMaxResults);
  };

  const handleClearCache = () => {
    queryClient.resetQueries();
  };

  return (
    <dialog id="modal" className="modal" onClose={onClose}>
      <div className="modal-box space-y-10">
        <p className="text-center text-2xl font-bold">Settings</p>
        <div className="flex w-full justify-center">
          <div className="flex w-[60%] flex-col gap-y-10">
            <div className="flex  items-center justify-between">
              <p>Theme</p>
              <label className="flex cursor-pointer gap-2">
                <Sun />
                <input
                  type="checkbox"
                  value={theme}
                  defaultChecked={theme === "dark"}
                  onChange={toggleTheme}
                  className="theme-controller toggle col-span-2 col-start-1 row-start-1 bg-base-content"
                />
                <Moon />
              </label>
            </div>
            <div className="flex items-center justify-between">
              <p>Max Results</p>
              <div>
                <input
                  type="range"
                  className="range"
                  min={0}
                  max={75}
                  step={25}
                  value={(maxResults - 1) * 25}
                  onChange={handleMaxResultsChange}
                />
                <div className="flex w-full justify-between px-2 text-xs">
                  <span>1</span>
                  <span>2</span>
                  <span>3</span>
                  <span>4</span>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <p>Clear cache</p>
              <button
                onClick={handleClearCache}
                type="button"
                className="btn flex items-center justify-center rounded-full border-none bg-transparent p-3"
              >
                <Trash2 />
              </button>
            </div>
          </div>
        </div>
        <div className="modal-action mt-10">
          <form method="dialog" className="space-x-2">
            <button className="btn">Close</button>
          </form>
        </div>
      </div>
    </dialog>
  );
};

export default SettingsModal;
