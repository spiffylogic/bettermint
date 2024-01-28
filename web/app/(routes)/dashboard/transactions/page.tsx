'use client'

import getUser from '@/app/lib/firebase/getUser';
import { Transaction } from '@/app/lib/model';
import * as server from  '@/app/services/bettermint';
import { lusitana } from "@/app/ui/fonts";
import TransactionsTable from "@/app/ui/transactions-table";

import { ArrowPathRoundedSquareIcon, ArrowsUpDownIcon } from '@heroicons/react/24/outline';
import { useEffect, useState } from "react";

export default function Transactions() {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const user = getUser();

    useEffect(() => {
        console.log("Transactions useEffect")
        clientRefresh()
    }, [user]);

    const clientRefresh = async () => {
        console.log("CLIENT REFRESH")
        if (user?.uid) {
            const data = await server.getTransactions(user?.uid);
            setTransactions(data);
            console.log(`Done ${data.length} rows`)
            return
        }
        setTransactions([]);
    }

    const serverRefresh = async () => {
        console.log("SERVER REFRESH")
        if (user?.uid) {
            const data = await server.syncTransactions(user?.uid);
            console.log(data);
            if (data && data.length == 3 && (data[0] > 0 || data[1] > 0 || data[2] > 0)) {
                clientRefresh();
            }
        }
    }

    return (
        <div className="w-full">
        <div className="flex w-full items-center justify-between">
          <h1 className={`${lusitana.className} text-2xl`}>Transactions</h1>
        </div>
        <div  className="mt-4 flex items-center justify-normal gap-2 md:mt-8">
            <button
                className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
                onClick={ clientRefresh }
            >
                <span className="hidden md:block">Refresh</span>{' '}
                <ArrowsUpDownIcon className="h-5 md:ml-4" />
            </button>
            <button
                className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
                onClick={ serverRefresh }
            >
                <span className="hidden md:block">Sync</span>{' '}
                <ArrowPathRoundedSquareIcon className="h-5 md:ml-4" />
            </button>
        </div>
        <TransactionsTable transactions={transactions} />
      </div>
    );
}
