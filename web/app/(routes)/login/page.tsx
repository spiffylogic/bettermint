'use client'

import { firebaseAuth, provider } from "@/app/lib/firebase/firebase-config";
import Logo from '@/app/ui/logo';

import { getRedirectResult, signInWithRedirect } from "firebase/auth";
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function LoginPage() {
  const router = useRouter()

  useEffect(() => {
    getRedirectResult(firebaseAuth).then(async (userCred) => {
      if (!userCred || !userCred?.user) {
        return;
      }

      const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
              identifier: userCred.user?.email,
              display_name: userCred.user?.displayName
          })
      };
      fetch(`http://localhost:5000/users/${userCred.user?.uid}`, requestOptions);
      fetch("/api/auth", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${await userCred.user.getIdToken()}`,
        },
      }).then((response) => {
        if (response.status === 200) {
          router.push("/dashboard");
        }
      });
    });
  }, [router]);

  function signIn() {
    signInWithRedirect(firebaseAuth, provider);
  }

  return (
    <main className="flex items-center justify-center md:h-screen">
      <div className="relative mx-auto flex w-full max-w-[400px] flex-col space-y-2.5 p-4 md:-mt-32">
        <div className="flex h-20 w-full items-end rounded-lg bg-blue-500 p-3 md:h-36">
          <div className="w-32 text-white md:w-36">
            <Logo />
          </div>
        </div>
        {/* <LoginForm /> */}
        <button onClick={signIn}>
          Sign In With Google
        </button>
      </div>
    </main>
  );
}
