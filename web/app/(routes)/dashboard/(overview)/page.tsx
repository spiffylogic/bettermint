'use client';

import getUser from "@/app/lib/firebase/getUser";

export default function Home() {
    const user = getUser();

    return (
        <main className="flex flex-col items-center justify-between p-24">
            <h1>DASHBOARD for { user ? user?.displayName : "Nobody" }
            </h1>
        </main>
    )
}