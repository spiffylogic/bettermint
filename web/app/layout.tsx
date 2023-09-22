'use client'

import './globals.css'
// import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Navbar from './navbar/navbar'
import UserContext from "./contexts/userContext";
import { useState } from 'react'

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
  const [user, setUserContext] = useState();
  return (
    <UserContext.Provider value={{user, setUserContext}}>
      <html lang="en">
        <body className={inter.className}>
          <Navbar />
          {children}
        </body>
      </html>
    </UserContext.Provider>
  )
}
