import getAuthenticatedAppForUser from "@/app/lib/firebase/getAuthenticatedAppForUser";
import SideNav from "@/app/ui/sidenav";

export default async function Layout({ children }: { children: React.ReactNode }) {
    const { currentUser } = await getAuthenticatedAppForUser();

    return (
        <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
            <div className="w-full flex-none md:w-64">
                <SideNav initialUser={currentUser ?? null} />
            </div>
            <div className="flex-grow p-6 md:overflow-y-auto md:p-12">{children}</div>
        </div>
    );
}