'use client'

import { useEffect } from "react";

export default function Accounts() {

    const getAccounts = async () => {
        const response = await fetch('http://localhost:5000/accounts', { method: 'GET' });
        const { accounts } = await response.json();
    };

    // get link_token from your server when component mounts
    useEffect(() => {
        getAccounts();
    }, []);


    return (
        <div>
            <h1>Accounts Page</h1>
        </div>
    );
}