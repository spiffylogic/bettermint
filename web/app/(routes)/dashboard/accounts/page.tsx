'use client'

import { useEffect, useState } from "react";
import { Account } from '@/app/lib/model';
import * as server from  '@/app/services/bettermint';
import getUser from "@/app/lib/firebase/getUser";

export default function Accounts() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const user = getUser();

    useEffect(() => {
        console.log("Accounts useEffect")
        if (user?.uid) {
            // self-invoking async function, since useEffect is not async
            (async() => {
                const data = await server.getAccounts(user?.uid);
                setAccounts(data);
            })()
        } else {
            setAccounts([]);
        }
    }, [user]);

    return (
        <div>
            <h1>Accounts Page</h1>
            <p>USERID: {user?.uid}</p>
            <center>
                { accounts.map((account: Account, index: number) => {
                    return (
                        <div key={index}>
                            <p>{ account.number  + " " + account.name }</p>
                        </div>
                    );
                })}
            </center>
        </div>
    );
}