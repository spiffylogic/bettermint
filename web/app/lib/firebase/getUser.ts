// This code was adapted from https://github.com/firebase/friendlyeats-web.git
// which comes from the code lab https://firebase.google.com/codelabs/firebase-nextjs

'use client';

import { User, onAuthStateChanged } from 'firebase/auth'
import { useEffect, useState } from 'react'

import { firebaseAuth } from '@/app/lib/firebase/firebase-config'
import { useRouter } from 'next/navigation'

export default function getUser(): User | null {
	const [user, setUser] = useState<User | null>(null)
	const router = useRouter()

	useEffect(() => {
		const unsubscribe = onAuthStateChanged(firebaseAuth, (authUser) => {
			setUser(authUser)
		})

		return () => unsubscribe()
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])

	useEffect(() => {
		onAuthStateChanged(firebaseAuth, (authUser) => {
			if (user === undefined) return

			// refresh when user changed to ease testing
			if (user?.email !== authUser?.email) {
				router.refresh()
			}
		})
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [user])

	return user
}
