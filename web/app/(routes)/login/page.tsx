'use client'

import { useContext, useEffect } from 'react';
import { User } from 'firebase/auth';

import Logo from '@/app/ui/logo';
import SignIn from '@/app/ui/sign-in';
import UserContext from '@/app/lib/userContext';
import { onAuthStateChangedHelper } from '@/app/lib/firebase';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const { user, setUser } = useContext(UserContext);
  const router = useRouter();

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
              router.push("/dashboard");
          }
      });

      // Cleanup subscription on unmount
      return () => unsubscribe();
  // empty dependency array means this effect will only run once (like componentDidMount in classes)
  }, []);

  return (
    <main className="flex items-center justify-center md:h-screen">
      <div className="relative mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4 md:-mt-32">
        <div className="flex h-20 w-full items-end rounded-lg bg-blue-500 p-3 md:h-36">
          <div className="w-32 text-white md:w-36">
            <Logo />
          </div>
        </div>
        {/* <LoginForm /> */}
        <SignIn user={user} />
      </div>
    </main>
  );
}