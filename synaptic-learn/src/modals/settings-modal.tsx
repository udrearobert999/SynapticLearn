import { useModal } from "@/hooks/use-modal-store";

const SettingsModal = () => {
  const { isOpen, type } = useModal();

  return (
    <dialog id="modal" className="modal">
      <div className="modal-box">
        <h3 className="text-lg font-bold">Hello!</h3>
        <p className="py-4">Press ESC key or click the button below to close</p>
        <div className="modal-action">
          <form method="dialog">
            <button className="btn">Close</button>
          </form>
        </div>
      </div>
    </dialog>
  );
};

export default SettingsModal;
