import { ChangeEvent, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { SendHorizontal } from "lucide-react";

interface QueryInputProps {
  onSubmit: () => void;
}

const QueryInput = ({ onSubmit }: QueryInputProps) => {
  const [isTyping, setIsTyping] = useState(false);

  const buttonVariants = {
    hidden: {
      x: "100%",
      opacity: 0,
    },
    visible: {
      x: "0%",
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 100,
        duration: 0.1,
      },
    },
    exit: {
      x: "0%",
      opacity: 0,
      transition: {
        easeOut: "linear",
        duration: 0.1,
      },
    },
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setIsTyping(e.currentTarget.value.length > 0);
  };

  return (
    <div className="relative w-[40%] overflow-hidden">
      <input
        className="input input-lg input-bordered w-full rounded-full pl-4 pr-20 focus:outline-none"
        placeholder="Search article..."
        onChange={handleInputChange}
      />
      <AnimatePresence>
        {isTyping && (
          <motion.button
            key={isTyping ? "visible" : "hidden"}
            onClick={onSubmit}
            className="btn absolute inset-y-2 right-1 flex items-center justify-center rounded-full border-none bg-transparent p-3"
            variants={buttonVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
          >
            <SendHorizontal />
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
};

export default QueryInput;
