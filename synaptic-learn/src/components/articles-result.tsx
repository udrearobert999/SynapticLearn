import { motion } from "framer-motion";
import Article from "@/components/article";
import { ArticleModel } from "@/models/article.model";

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
    transition: { duration: 0.5 },
  },
};

interface ArticleResult {
  articles: ArticleModel[];
}

const ArticlesResult = ({ articles }: ArticleResult) => {
  if (articles.length === 0) {
    return (
      <div className="flex flex-grow items-center justify-center">
        <p>No similar articles found!</p>
      </div>
    );
  }

  return (
    <div className="flex h-full items-center justify-center overflow-y-auto py-20">
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

export default ArticlesResult;
