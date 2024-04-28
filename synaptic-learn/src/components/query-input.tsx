import { ChangeEvent, useRef, useState, FormEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { SendHorizontal } from "lucide-react";

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

interface QueryInputProps {
  onSubmit: (query: string) => void;
}

const QueryInput = ({ onSubmit }: QueryInputProps) => {
  const [isTyping, setIsTyping] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setIsTyping(e.currentTarget.value.length > 0);
  };

  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (inputRef.current) {
      onSubmit(inputRef.current.value);
    }
  };

  return (
    <form
      className="relative w-[40%] overflow-hidden"
      onSubmit={handleFormSubmit}
    >
      <input
        className="input input-lg input-bordered w-full rounded-full pl-4 pr-20 focus:outline-none"
        placeholder="Search article..."
        onChange={handleInputChange}
        ref={inputRef}
        required
      />
      <AnimatePresence>
        {isTyping && (
          <motion.button
            key={isTyping ? "visible" : "hidden"}
            type="submit"
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
    </form>
  );
};

export default QueryInput;
