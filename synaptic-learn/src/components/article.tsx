import { ArticleModel } from "@/models/article.model";
import { ArrowBigRight } from "lucide-react";

interface ArticleProps {
  article: ArticleModel;
}

const Article = ({ article }: ArticleProps) => {
  const { title, text, url, label } = article;

  const handleGoToPage = () => {
    window.open(url, "_blank", "noopener,noreferrer");
  };

  return (
    <div className="card -z-10 w-96 bg-neutral text-neutral-content shadow-xl">
      <div className="card-body flex gap-4">
        <div className="card-title flex items-center justify-between gap-4">
          <p className="flex-1 truncate font-bold">{title}</p>
          <span className="badge">{label}</span>
        </div>
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
