import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const fetchModelPlot = async (plotUrl: string): Promise<string> => {
  const { data } = await axios.get(plotUrl, {
    responseType: "text",
  });

  return data;
};

interface ModelPlotProps {
  plotUrl: string;
}

const ModelPlot = ({ plotUrl }: ModelPlotProps) => {
  const query = useQuery<string, Error>({
    queryKey: ["model-plot", plotUrl],
    queryFn: () => fetchModelPlot(plotUrl),
  });

  if (query.isLoading)
    return (
      <div className="flex flex-grow items-center justify-center">
        <span className="loading loading-spinner h-14 w-14"></span>
      </div>
    );
  if (query.error)
    return (
      <div className="flex flex-grow items-center justify-center">
        <p>Error fetching the plot!</p>
      </div>
    );

  return (
    <iframe
      srcDoc={query.data}
      className="h-full w-full"
      title="Base Model Plot"
    />
  );
};

export default ModelPlot;
