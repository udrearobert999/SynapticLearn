import AppTitle from "@/components/app-title";
import Article from "@/components/article";
import QueryInput from "@/components/query-input";
import SettingsButton from "@/components/settings-button";
import { useModal } from "@/hooks/use-modal-store";
import { ArticleModel } from "@/models/article.model";
import { motion } from "framer-motion";
import { useState } from "react";

const articleList: ArticleModel[] = [
  {
    id: 1,
    title: "Ecotype",
    label: "Zoology",
    url: "https://www.google.com/",
    text: "In evolutionary ecology, an ecotype, sometimes called ecospecies, describes a genetically distinct geographic variety, population, or race within a species, which is genotypically adapted to specific environmental conditions.",
  },
  {
    id: 2,
    title: "Ecotype2",
    label: "Zoology",
    url: "https://www.google.com/",
    text: "In evolutionary ecology, an ecotype, sometimes called ecospecies, describes a genetically distinct geographic variety, population, or race within a species, which is genotypically adapted to specific environmental conditions.",
  },
  {
    id: 3,
    title: "Ecotype3",
    label: "Zoology",
    url: "https://www.google.com/",
    text: "In evolutionary ecology, an ecotype, sometimes called ecospecies, describes a genetically distinct geographic variety, population, or race within a species, which is genotypically adapted to specific environmental conditions.",
  },
  {
    id: 4,
    title: "Ecotype4",
    label: "Zoology",
    url: "https://www.google.com/",
    text: "In evolutionary ecology, an ecotype, sometimes called ecospecies, describes a genetically distinct geographic variety, population, or race within a species, which is genotypically adapted to specific environmental conditions.",
  },
];

const HomePage = () => {
  const [articles, setArticles] = useState<ArticleModel[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { onOpen } = useModal();

  const onSubmitQuery = () => {
    setIsLoading(true);

    setTimeout(() => {
      setArticles(articleList);
      setIsLoading(false);
    }, 2000);
  };

  const containerVariants = {
    hidden: { opacity: 1, scale: 0.5 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        staggerChildren: 0.15,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
      },
    },
  };
  const renderArticleResults = () => {
    return (
      <div className="flex h-full items-center justify-center overflow-y-auto">
        <motion.div
          className="flex h-full w-1/2 flex-wrap items-center justify-center gap-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {articles.map((article) => (
            <motion.div key={article.id} variants={itemVariants}>
              <Article article={article} />
            </motion.div>
          ))}
        </motion.div>
      </div>
    );
  };

  return (
    <div className="flex h-[90dvh] w-dvw flex-col overflow-hidden">
      {isLoading ? (
        <div className="flex flex-grow items-center justify-center">
          <span className="loading loading-spinner h-14 w-14"></span>
        </div>
      ) : articles.length === 0 ? (
        <div className="flex flex-grow items-center justify-center">
          <AppTitle />
        </div>
      ) : (
        renderArticleResults()
      )}
      <div className="fixed bottom-0 left-0 right-0 flex w-full items-center justify-center border-t-2 border-gray-600/20 p-4">
        <QueryInput onSubmit={onSubmitQuery} />
        <SettingsButton onClick={() => onOpen("settings")} />
      </div>
    </div>
  );
};

export default HomePage;
