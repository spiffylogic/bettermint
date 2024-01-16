'use client';

import { useContext } from "react";
import UserContext from '@/app/lib/userContext';

export default function Home() {
    const { user } = useContext(UserContext);

    return (
        <main className="flex flex-col items-center justify-between p-24">
            <h1>DASHBOARD for { user ? user?.displayName : "Nobody" }
            </h1>
        </main>
    )
}