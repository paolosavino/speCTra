import { KeyList } from "@/components/api-keys/KeyList";
import { CreateKeyModal } from "@/components/api-keys/CreateKeyModal";

export default function ApiKeysPage() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">API Keys</h1>
                    <p className="text-muted-foreground">
                        Manage your API keys for accessing the speCTra Gateway.
                    </p>
                </div>
                <CreateKeyModal />
            </div>
            <KeyList />
        </div>
    );
}
