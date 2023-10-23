'use client'

import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import UserContext from '../contexts/userContext'
import {
    usePlaidLink,
    // PlaidLinkOptions,
    PlaidLinkOnSuccess,
    PlaidAccount,
  } from 'react-plaid-link';
import { createLinkToken } from '../services/bettermint';

export default function Link() {
    const [token, setToken] = useState<string | null>(null);
    const { user } = useContext(UserContext);

    // These seems to be necessary otherwise we lose the user
    // when the component is recreated after returning from the Link UI
    const userRef = useRef(user);
    userRef.current = user;

    async function setAccessToken(publicToken: string, userId: string | null) {
        console.log(`Sending public token ${publicToken} for user ${userId}`);
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                public_token: publicToken
            })
        };
        const response = await fetch('http://localhost:5000/set_access_token', requestOptions);
    };

    async function saveAccounts(accounts: Array<PlaidAccount>, userId: string) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                accounts: accounts.map((value: PlaidAccount, index: number, array: PlaidAccount[]) => {
                    return {
                        name: value.name,
                        number: value.mask
                    }
                })
            })
        };
        const response = await fetch(`http://localhost:5000/accounts?user_id=${userId}`, requestOptions);
    }

    // get link_token from your server when component mounts
    useEffect(() => {
        // self-invoking async function, since useEffect is not async
        (async() => {
            const link_token = await createLinkToken();
            setToken(link_token);
        })()
    }, []);

    const onSuccess = useCallback<PlaidLinkOnSuccess>((publicToken, metadata) => {
      // https://plaid.com/docs/api/tokens/#token-exchange-flow
      if (userRef.current) {
        const userId = userRef.current?.uid;
        setAccessToken(publicToken, userId);
        saveAccounts(metadata.accounts, userId);
      }
    }, []);

    const { open, ready } = usePlaidLink({
      token,
      onSuccess,
      // onEvent
      // onExit
    });

    return (
        <div>
            <p>USERID: {user?.uid}</p>
            <button onClick={() => open()} disabled={!ready}>
                Connect a bank account
            </button>
        </div>
    );
}