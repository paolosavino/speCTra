import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Trash2, Copy, Eye, EyeOff } from "lucide-react";
import api from "@/lib/api";
import { toast } from "sonner";
import { useState } from "react";

interface ApiKey {
    id: number;
    name: string;
    key_hash: string;
    is_active: boolean;
    created_at: string;
}

export function KeyList() {
    const queryClient = useQueryClient();
    const { data: keys, isLoading, error } = useQuery<ApiKey[]>({
        queryKey: ["api-keys"],
        queryFn: async () => {
            const res = await api.get("/v1/api-keys");
            return res.data;
        },
    });

    const deleteMutation = useMutation({
        mutationFn: async (id: number) => {
            await api.delete(`/v1/api-keys/${id}`);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["api-keys"] });
            toast.success("API Key deleted");
        },
    });

    const [visibleKeys, setVisibleKeys] = useState<Record<number, boolean>>({});

    const toggleVisibility = (id: number) => {
        setVisibleKeys(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
        toast.success("Key copied to clipboard");
    };

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error loading keys</div>;

    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Key</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Created At</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {keys?.map((key) => (
                        <TableRow key={key.id}>
                            <TableCell className="font-medium">{key.name}</TableCell>
                            <TableCell className="font-mono text-sm max-w-[200px] truncate">
                                {visibleKeys[key.id] ? key.key_hash : "sk-speCTra-••••••••"}
                            </TableCell>
                            <TableCell>
                                <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
                                    Active
                                </span>
                            </TableCell>
                            <TableCell>{new Date(key.created_at).toLocaleDateString()}</TableCell>
                            <TableCell className="text-right space-x-2">
                                <Button variant="ghost" size="icon" onClick={() => toggleVisibility(key.id)}>
                                    {visibleKeys[key.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                </Button>
                                <Button variant="ghost" size="icon" onClick={() => copyToClipboard(key.key_hash)}>
                                    <Copy className="h-4 w-4" />
                                </Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="text-destructive hover:text-destructive"
                                    onClick={() => deleteMutation.mutate(key.id)}
                                >
                                    <Trash2 className="h-4 w-4" />
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                    {keys?.length === 0 && (
                        <TableRow>
                            <TableCell colSpan={5} className="text-center h-24 text-muted-foreground">
                                No API Keys found. Create one to get started.
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
}
