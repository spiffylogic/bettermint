'use client'

import { useContext, useEffect, useState } from "react";
import UserContext from '../../contexts/userContext';
import { Account } from '../../types/account';
import * as server from  '../../services/bettermint';

export default function Accounts() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const { user } = useContext(UserContext);

    useEffect(() => {
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