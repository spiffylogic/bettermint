// This code was adapted from https://github.com/firebase/friendlyeats-web.git
// which comes from the code lab https://firebase.google.com/codelabs/firebase-nextjs

'use client';

import { onAuthStateChanged } from '@/app/lib/firebase/auth';
import { User } from 'firebase/auth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function useUserSession(initialUser: User | null) {
    // The initialUser comes from the server via a server component
    const [user, setUser] = useState<User | null>(initialUser);
    const router = useRouter();

    useEffect(() => {
        const unsubscribe = onAuthStateChanged((authUser) => {
            setUser(authUser);
        });
        return () => unsubscribe();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        onAuthStateChanged((authUser) => {
            if (user === undefined) return;
            // refresh when user changed to ease testing
            if (user?.email !== authUser?.email) {
                router.refresh();
            }
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [user]);

    return user;
}
