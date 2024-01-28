'use client'

import { onAuthStateChanged, signInWithGoogle } from '@/app/lib/firebase/auth';
import Logo from '@/app/ui/logo';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function LoginPage() {
  const router = useRouter()

  useEffect(() => {
		const unsubscribe = onAuthStateChanged((user) => {
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
        router.push("/dashboard");
      };
    });

		return () => unsubscribe();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])

  return (
    <main className="flex items-center justify-center md:h-screen">
      <div className="relative mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4 md:-mt-32">
        <div className="flex h-20 w-full items-end rounded-lg bg-blue-500 p-3 md:h-36">
          <div className="w-32 text-white md:w-36">
            <Logo />
          </div>
        </div>
        {/* <LoginForm /> */}
        <button onClick={signInWithGoogle}>
          Sign In With Google
        </button>
      </div>
    </main>
  );
}