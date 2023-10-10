'use client'

import { useContext, useEffect, useState } from "react";
import UserContext from '../contexts/userContext';

interface Account {
    number: string;
    name: string;
}

export default function Accounts() {
    const [accounts, setAccounts] = useState([]);
    const { user } = useContext(UserContext);

    const getAccounts = async () => {
        const response = await fetch(`http://localhost:5000/accounts?user_id=${user?.uid}`, { method: 'GET' });
        const data = await response.json();
        setAccounts(data);
    };

    useEffect(() => {
        getAccounts();
    }, [user]);

    return (
        <div>
            <h1>Accounts Page</h1>
            <p>USERID: {user?.uid}</p>
            <center>
                { accounts.map((account: Account, index) => {
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