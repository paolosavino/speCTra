import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";
import { Key } from "lucide-react";

export default function Dashboard() {
    const { data: keys, isLoading } = useQuery({
        queryKey: ["api-keys"],
        queryFn: async () => {
            const res = await api.get("/v1/api-keys");
            return res.data;
        },
    });

    const activeKeysCount = keys?.filter((k: any) => k.is_active).length || 0;
    const totalKeysCount = keys?.length || 0;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-muted-foreground">
                    Overview of your Gateway usage.
                </p>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Keys</CardTitle>
                        <Key className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{isLoading ? "..." : activeKeysCount}</div>
                        <p className="text-xs text-muted-foreground">
                            out of {totalKeysCount} total keys
                        </p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
