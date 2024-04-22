import AppTitle from "@/components/app-title";
import QueryInput from "@/components/query-input";

const HomePage = () => {
  return (
    <div className="flex h-screen flex-col">
      <div className="flex flex-grow items-center justify-center">
        <AppTitle />
      </div>
      <div className="fixed bottom-0 left-0 right-0 flex w-full justify-center border-t-2 border-gray-600/20 p-4">
        <QueryInput />
      </div>
    </div>
  );
};

export default HomePage;
