'use client';

import { signOut } from '@/app/lib/firebase/auth';
import useUserSession from '@/app/lib/firebase/useUserSession';

import { User } from 'firebase/auth';
import { ArrowRightIcon, PowerIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Fragment } from 'react';

interface SignInProps {
    initialUser: User | null
}

export default function SignIn({ initialUser }: SignInProps) {
    const router = useRouter();
    const user = useUserSession(initialUser);

    return (
        <Fragment>
            { user ?
                (
                    <button
                        onClick={() => {
                            signOut();
                            router.push("/");
                        }}
                        className="flex h-[48px] w-full grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3"
                    >
                        <PowerIcon className="w-6" />
                        <div className="hidden md:block">Sign Out</div>
                    </button>
                ) : (
                    <Link
                        href="/login"
                        className="flex items-center gap-5 self-start rounded-lg bg-blue-500 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-blue-400 md:text-base"
                    >
                        <span>Log in</span> <ArrowRightIcon className="w-5 md:w-6" />
                    </Link>
                )
            }
        </Fragment>
    )
}
