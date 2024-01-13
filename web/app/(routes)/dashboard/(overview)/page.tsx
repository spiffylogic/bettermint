import { GoogleLoginButton, LogoutButton } from "@/app/ui/login-form";
import { getServerSession } from "next-auth";

export default async function Home() {
    // Important: this can only be used in server components.
    // So buttons must be in separate files as client components.
    const session = await getServerSession();
    return (
        <main className="flex flex-col items-center justify-between p-24">
            <h1>DASHBOARD HOME</h1>
            <h1>{session?.user?.name}</h1>
            {!session?.user && <GoogleLoginButton/>}
            { session?.user && <LogoutButton/>}
        </main>
    )
}