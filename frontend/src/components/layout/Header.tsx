// We will need a mode toggle, or just basic user menu
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function Header() {
    return (
        <header className="border-b bg-card">
            <div className="flex h-16 items-center px-4 w-full justify-between">
                <div className="md:hidden">
                    {/* Mobile Menu Trigger would go here */}
                    <span className="font-bold">speCTra</span>
                </div>
                <div className="ml-auto flex items-center space-x-4">
                    {/* Placeholder for Theme Toggle */}
                    <div className="text-sm text-muted-foreground mr-4">User: Admin</div>
                    <Avatar>
                        <AvatarImage src="https://github.com/shadcn.png" />
                        <AvatarFallback>CN</AvatarFallback>
                    </Avatar>
                </div>
            </div>
        </header>
    );
}
