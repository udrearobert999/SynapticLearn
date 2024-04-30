import { ChangeEvent, FormEvent, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Paperclip, SendHorizontal, X } from "lucide-react";

const buttonsVariants = {
  hidden: {
    x: 50,
    transition: {
      type: "linear",
      duration: 0.2,
    },
  },
  visible: {
    x: 0,
    transition: {
      type: "linear",
      duration: 0.2,
    },
  },
  exit: {
    x: 50,
    transition: {
      type: "linear",
      duration: 0.2,
    },
  },
};

interface QueryInputProps {
  onSubmit: (query: string, file?: File) => void;
}

const QueryInput = ({ onSubmit }: QueryInputProps) => {
  const [query, setQuery] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [file, setFile] = useState<File | undefined>(undefined);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    setIsTyping(Boolean(displayText));
  }, [displayText]);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    setDisplayText(newQuery);
  };

  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query) {
      onSubmit(query);
    }
  };

  const handleFileInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (file) {
      if (!file.name.toLowerCase().endsWith(".txt")) {
        throw new Error("Please select a text file (.txt)");
      }

      setFile(file);
      setDisplayText(file.name);
      const reader = new FileReader();

      reader.onload = (event) => {
        const content = event.target?.result as string;
        setQuery(content);
      };

      reader.readAsText(file);
    }
  };

  const handleRemoveFile = () => {
    setFile(undefined);
    setDisplayText("");
  };

  const handleAddFile = () => {
    fileInputRef.current?.click();
  };

  return (
    <form
      className="relative w-[40%] overflow-hidden"
      onSubmit={handleFormSubmit}
    >
      <input
        className={`input input-lg input-bordered w-full rounded-full pl-4 pr-28 focus:outline-none ${!file ? undefined : "font-bold"}`}
        placeholder="Search article..."
        onChange={handleInputChange}
        disabled={file !== undefined}
        value={displayText}
        required
      />
      <input
        type="file"
        className="hidden"
        onChange={handleFileInputChange}
        ref={fileInputRef}
        accept=".txt"
      />
      <AnimatePresence>
        <motion.div
          className="absolute inset-y-0 right-0 flex items-center space-x-1 pr-1"
          variants={buttonsVariants}
          initial="hidden"
          animate={isTyping ? "visible" : "hidden"}
          exit="exit"
        >
          {file !== undefined && (
            <button
              type="button"
              className="btn flex items-center justify-center rounded-full border-none bg-transparent p-3"
              onClick={handleRemoveFile}
            >
              <X />
            </button>
          )}
          {file === undefined && (
            <button
              type="button"
              className="btn flex items-center justify-center rounded-full border-none bg-transparent p-3"
              onClick={handleAddFile}
            >
              <Paperclip />
            </button>
          )}
          <button
            type="submit"
            className="btn flex items-center justify-center rounded-full border-none bg-transparent p-3"
          >
            <SendHorizontal />
          </button>
        </motion.div>
      </AnimatePresence>
    </form>
  );
};

export default QueryInput;
