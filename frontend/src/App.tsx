import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "@/components/layout/Layout";

import Dashboard from "@/pages/Dashboard";
import ApiKeysPage from "@/pages/ApiKeys";

const Playground = () => <div className="text-2xl font-bold">Playground (Coming Soon)</div>;
const SettingsPage = () => <div className="text-2xl font-bold">Settings (Coming Soon)</div>;

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="api-keys" element={<ApiKeysPage />} />
            <Route path="playground" element={<Playground />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
