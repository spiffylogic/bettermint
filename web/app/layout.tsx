import '@/app/ui/globals.css'
import { ThemeProvider } from "@/app/ui/material";

import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'Bettermint',
    description: 'Better than Mint',
}

export default async function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <ThemeProvider>
            <html lang="en">
                <body className={`${inter.className} antialiased`}>
                    {children}
                </body>
            </html>
        </ThemeProvider>
    )
}
