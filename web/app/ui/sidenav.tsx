'use client';

import { onAuthStateChangedHelper } from '@/app/lib/firebase';
import UserContext from '@/app/lib/userContext';
import Logo from '@/app/ui/logo';
import NavLinks from '@/app/ui/nav-links';
import SignIn from '@/app/ui/sign-in';

import { User } from 'firebase/auth';
import Link from 'next/link';
import { useContext, useEffect } from 'react';

export default function SideNav() {
  const { user, setUser } = useContext(UserContext);

  useEffect(() => {
      const unsubscribe = onAuthStateChangedHelper((user: User | null) => {
          setUser(user);
      });
      // Cleanup subscription on unmount
      return () => unsubscribe();
  // empty dependency array means this effect will only run once (like componentDidMount in classes)
  }, []);

  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
        <Link
            className="mb-2 flex h-20 items-end justify-start rounded-md bg-blue-600 p-4 md:h-40"
            href="/"
        >
        <div className="w-32 text-white md:w-40">
            <Logo />
        </div>
      </Link>
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <NavLinks />
        <div className="hidden h-auto w-full grow rounded-md bg-gray-50 md:block"></div>
            <SignIn user={user} />
        </div>
    </div>
  );
}
