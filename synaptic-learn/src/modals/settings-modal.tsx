import { useMaxResults } from "@/hooks/use-max-results";
import { useModal } from "@/hooks/use-modal-store";
import { useTheme } from "@/hooks/use-theme";
import { ChangeEvent, useEffect } from "react";

const SettingsModal = () => {
  const { isOpen, type, onClose } = useModal();
  const { theme, toggleTheme } = useTheme();
  const { maxResults, setMaxResults } = useMaxResults();

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
    const result = Number(e.currentTarget.value) / Number(e.currentTarget.step);
    setMaxResults(result + 1);
  };

  return (
    <dialog id="modal" className="modal" onClose={onClose}>
      <div className="modal-box space-y-10">
        <p className="text-center text-2xl font-bold">Settings</p>
        <div className="flex w-full justify-center">
          <div className="flex w-[60%] flex-col gap-y-10">
            <div className="flex  items-center justify-between">
              <p>Theme</p>
              <label className="grid cursor-pointer place-items-center">
                <input
                  type="checkbox"
                  value={theme}
                  defaultChecked={theme === "dark"}
                  onChange={toggleTheme}
                  className="theme-controller toggle col-span-2 col-start-1 row-start-1 bg-base-content"
                />
                <svg
                  className="col-start-1 row-start-1 fill-base-100 stroke-base-100"
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="12" cy="12" r="5" />
                  <path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
                </svg>
                <svg
                  className="col-start-2 row-start-1 fill-base-100 stroke-base-100"
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
              </label>
            </div>
            <div className="flex items-center justify-between">
              <p>Max Results</p>
              <div>
                <input
                  type="range"
                  className="range range-primary"
                  min={0}
                  max={100}
                  step={25}
                  defaultValue={(maxResults - 1) * 25}
                  onChange={handleMaxResultsChange}
                />
                <div className="flex w-full justify-between px-2 text-xs">
                  <span>1</span>
                  <span>2</span>
                  <span>3</span>
                  <span>4</span>
                  <span>5</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-action mt-10">
          <form method="dialog" className="space-x-2">
            <button className="btn">Close</button>
            <button className="btn btn-primary">Save</button>
          </form>
        </div>
      </div>
    </dialog>
  );
};

export default SettingsModal;
