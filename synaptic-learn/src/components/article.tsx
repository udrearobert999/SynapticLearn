import { ArticleModel } from "@/models/article.model";
import { ArrowBigRight } from "lucide-react";

interface ArticleProps {
  article: ArticleModel;
}

const Article = ({ article }: ArticleProps) => {
  let { title, label, text, url } = article;

  const handleGoToPage = () => {
    window.location.href = url;
  };

  return (
    <div className="card w-96 bg-neutral text-neutral-content shadow-xl">
      <div className="card-body">
        <h2 className="card-title">{title}</h2>
        <p className="line-clamp-4">{text}</p>
        <div className="card-actions justify-end">
          <button onClick={handleGoToPage} className="btn">
            Go <ArrowBigRight />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Article;
