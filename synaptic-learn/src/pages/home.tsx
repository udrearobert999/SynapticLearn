import { useQuery } from "@tanstack/react-query";
import { axiosClient } from "@/axios";
import QueryInput from "@/components/query-input";
import SettingsButton from "@/components/settings-button";
import { useModal } from "@/hooks/use-modal-store";
import { useSettingsStore } from "@/hooks/use-settings-store";
import { ArticleModel } from "@/models/article.model";
import { useState } from "react";
import ArticlesResult from "@/components/articles-result";
import AppTitle from "@/components/app-title";
import { MoveRight } from "lucide-react";
import { NavLink } from "react-router-dom";

const fetchArticles = async (
  query: string,
  maxResults: number,
): Promise<ArticleModel[]> => {
  const response = await axiosClient.post(
    "/similar-articles",
    { query },
    {
      params: {
        maxResults: maxResults,
      },
    },
  );

  return response.data;
};

const HomePage = () => {
  const [query, setQuery] = useState<string | null>(null);
  const { onOpen } = useModal();
  const { maxResults } = useSettingsStore();

  const {
    data: articles,
    isLoading,
    isError,
    refetch,
  } = useQuery<ArticleModel[]>({
    queryKey: ["articles", query, maxResults],
    queryFn: () => fetchArticles(query ?? "", maxResults),
    enabled: !!query,
    refetchOnWindowFocus: false,
  });

  const onSubmitQuery = (newQuery: string) => {
    setQuery(newQuery);
    if (isError) refetch();
  };

  return (
    <div className="relative flex h-[90dvh] w-dvw flex-col overflow-hidden">
      <button className="btn btn-primary absolute right-20 top-14 w-44 rounded-full">
        <NavLink
          to="/plots"
          className="flex h-full w-full items-center justify-center gap-4"
        >
          See plots <MoveRight />
        </NavLink>
      </button>
      {isLoading && (
        <div className="flex flex-grow items-center justify-center">
          <span className="loading loading-spinner h-14 w-14"></span>
        </div>
      )}
      {isError && (
        <div className="flex flex-grow items-center justify-center">
          <p>Error fetching articles! Please try again later!</p>
        </div>
      )}
      {!articles && !isLoading && !isError && (
        <div className="flex flex-grow items-center justify-center">
          <AppTitle />
        </div>
      )}
      {!isLoading && !isError && articles && (
        <ArticlesResult articles={articles} />
      )}
      <div className="fixed bottom-0 left-0 right-0 flex min-h-28 w-full items-center justify-center border-t-2 border-gray-600/20 bg-base-100">
        <QueryInput onSubmit={onSubmitQuery} />
        <SettingsButton onClick={() => onOpen("settings")} />
      </div>
    </div>
  );
};

export default HomePage;
