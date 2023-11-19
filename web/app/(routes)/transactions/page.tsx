'use client'

import { useContext, useEffect, useState } from "react";
import UserContext from '../../contexts/userContext';
import { Transaction } from '../../types/model';
import * as server from  '../../services/bettermint';

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
        }
    }

    return (
        <div>
            <h1>{ transactions.length } transactions for user { user?.uid }</h1>

            {/* <button type="button" className="btn btn-outline-secondary button-md my-2" id="serverRefresh">Server refresh</button> */}
            <button className="btn-primary" onClick={ clientRefresh }>Client Refresh</button>
            <button className="btn-primary" onClick={ serverRefresh }>Server Refresh</button>

            <table className="border-collapse table-auto w-full text-sm">
                <thead>
                <tr>
                    <th className="border-b dark:border-slate-600 font-medium p-4 pl-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Date</th>
                    <th className="border-b dark:border-slate-600 font-medium p-4 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Name</th>
                    <th className="border-b dark:border-slate-600 font-medium p-4 pr-8 pt-0 pb-3 text-slate-400 dark:text-slate-200 text-left">Amount</th>
                </tr>
                </thead>
                <tbody className="bg-white dark:bg-slate-800">
                { transactions.map((transaction: Transaction, index: number) => {
                    return (
                        <tr key={ index }>
                        <td className="border-b border-slate-100 dark:border-slate-700 p-4 pl-8 text-slate-500 dark:text-slate-400">{ new Date(transaction.date).toLocaleDateString() }</td>
                        <td className="border-b border-slate-100 dark:border-slate-700 p-4 text-slate-500 dark:text-slate-400">{ transaction.name }</td>
                        <td className="border-b border-slate-100 dark:border-slate-700 p-4 pr-8 text-slate-500 dark:text-slate-400">{ transaction.amount }</td>
                    </tr>
                    );
                })}
                </tbody>
            </table>
        </div>
    );
}