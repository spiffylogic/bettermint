'use client';

import UserContext from '../contexts/userContext';
import { onAuthStateChangedHelper } from '../firebase/firebase';
import SignIn from './sign-in';

import { User } from 'firebase/auth';
import Image from 'next/image';
import Link from 'next/link';
import { useContext, useEffect } from 'react';

// Note: This react function component is an example of a JavaScript closure.
// State is maintained inside the function, via useState, even after it returns.
export default function Navbar() {
    // Init user state
    const { user, setUser } = useContext(UserContext);

    useEffect(() => {
        const unsubscribe = onAuthStateChangedHelper((user: User | null) => {
            setUser(user);
            if (user && user?.uid) {
                const requestOptions = {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        identifier: user?.email,
                        display_name: user?.displayName
                    })
                };
                fetch(`http://localhost:5000/users/${user?.uid}`, requestOptions);
            }
        });

        // Cleanup subscription on unmount
        return () => unsubscribe();
    // empty dependency array means this effect will only run once (like componentDidMount in classes)
    }, []);

    return (
        <nav className="flex flex-row justify-center items-baseline space-x-4 py-10">
            <Link href="/">
                <Image src="/mint.svg"  width={128} height={128} alt="Logo" />
            </Link>
            <div className="text-3xl font-bold">bettermint</div>
            <SignIn user={user} />
        </nav>
    );
}