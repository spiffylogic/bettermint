'use client'

import './globals.css'
// import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Navbar from './ui/navbar'
import AppContext from "./lib/userContext";
import { useState } from 'react'
import { UserContext } from './lib/globalContext';
import { User } from 'firebase/auth';

const inter = Inter({ subsets: ['latin'] })

// export const metadata: Metadata = {
//   title: 'Bettermint',
//   description: 'Better than Mint',
// }

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [context, setContext] = useState<UserContext>({} as UserContext);
  const [user,setUser] = useState<User | null>(null);
  return (
    <AppContext.Provider value={{...context, setContext,user,setUser}}>
      <html lang="en">
        <body className={inter.className}>
          <Navbar />
          {children}
        </body>
      </html>
    </AppContext.Provider>
  )
}
