'use client';

import useUser from '@/app/lib/firebase/getUser';
import { ArrowRightIcon, PowerIcon } from '@heroicons/react/24/outline';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Fragment } from 'react';

export default function SignIn() {
    const router = useRouter();
    const user = useUser();

    return (
        <Fragment>
            { user ?
                (
                    <button
                        onClick={() => {
                            fetch("/api/auth", { method: "DELETE" }).then((response) => {
                                if (response.status === 200) {
                                    router.push("/");
                                }
                            });
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
