'use client'

import { lusitana } from '@/app/ui/fonts';
import { signIn, signOut } from 'next-auth/react';

export default function LoginForm() {
  return (
    // NOTE: since this is a form the button onClick event submits is by default
    // action={dispatch}
    <>
    <form className="space-y-3">
      <div className="flex-1 rounded-lg bg-gray-50 px-6 pb-4 pt-8">
        <h1 className={`${lusitana.className} mb-3 text-2xl`}>
          Please log in to continue.
        </h1>
        (email/password login coming soon)
      </div>
    </form>
    <GoogleLoginButton />
    </>
  );
}

export function GoogleLoginButton() {
  return (
    <button onClick={() => signIn('google', { callbackUrl: "/dashboard" })}>
      Login with Gurgle
    </button>
  );
}

export function LogoutButton() {
    return (
        <button onClick={() => signOut({ callbackUrl: "/"})}>Logout</button>
    );
}