'use client';

import { onAuthStateChangedHelper } from '../firebase/firebase';
import SignIn from './sign-in';

import { User } from 'firebase/auth';
import Image from 'next/image';
import Link from 'next/link';
import { useEffect, useState } from 'react';

// Note: This react function component is an example of JavaScript closures.
// State is maintained inside the function, via useState, even after it returns.
export default function Navbar() {
    // Init user state
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const unsubscribe = onAuthStateChangedHelper((user) => {
            console.log(`onAuthStateChangedHelper ${user?.displayName} ${ user?.email} ${ user?.uid}`)
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
                fetch(`http://localhost:5000/users/${user?.uid}`, requestOptions)
                    .then(response => response.json())
                    .then(data => {
                        console.log("MARKUS");
                    });
            }
        });

        // Cleanup subscription on unmount
        return () => unsubscribe();
    // empty dependency array means this effect will only run once (like componentDidMount in classes)
    }, []);

    return (
        <nav>
            <Link href="/">
                <Image src="/mint.svg"  width={128} height={128} alt="Logo" />
            </Link>
            <SignIn user={user} />
        </nav>
    );
}