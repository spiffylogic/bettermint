'use client'

import { Transaction } from '@/app/lib/model';
import UserContext from '@/app/lib/userContext';
import * as server from  '@/app/services/bettermint';
import { lusitana } from "@/app/ui/fonts";
import TransactionsTable from "@/app/ui/transactions-table";

import { useContext, useEffect, useState } from "react";

export default function Transactions() {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const { user } = useContext(UserContext);

    useEffect(() => {
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
        <div>
            <button className="btn-primary" onClick={ clientRefresh }>Client Refresh</button><br/>
            <button className="btn-primary" onClick={ serverRefresh }>Server Refresh</button>
        </div>
        <TransactionsTable transactions={transactions} />
      </div>
    );
}