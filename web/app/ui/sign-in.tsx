'use client';

import { signInWithGoogle, signOut } from '../lib/firebase';

import { User } from 'firebase/auth';
import { Fragment } from 'react';

interface SignInProps {
    user: User | null
}
// Note: this is called descructing assignment (instead of using props: SignInProps)
export default function SignIn({ user }: SignInProps) {
    return (
        <Fragment>
            { user ?
            (
                <button onClick={signOut}>
                    Sign Out
                </button>
            ) : (
                <button onClick={signInWithGoogle}>
                    Sign In
                </button>
            )
            }
        </Fragment>
    )
}