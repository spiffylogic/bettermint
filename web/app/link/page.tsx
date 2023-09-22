'use client'

import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import UserContext from '../contexts/userContext'
import {
    usePlaidLink,
    PlaidLinkOptions,
    PlaidLinkOnSuccess,
  } from 'react-plaid-link';

export default function Link() {
    const [token, setToken] = useState<string | null>(null);
    const { user } = useContext(UserContext);
    console.log("User from context: ", user)

    // These seems to be necessary otherwise we lose the user
    // when the component is recreated after returning from the Link UI
    const userRef = useRef(user);
    userRef.current = user;

    const createLinkToken = async () => {
        const response = await fetch('http://localhost:5000/create_link_token', { method: 'POST' });
        const { link_token } = await response.json();
        setToken(link_token);
    };

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

    // get link_token from your server when component mounts
    useEffect(() => {
        createLinkToken();
    }, []);

    const onSuccess = useCallback<PlaidLinkOnSuccess>((publicToken, metadata) => {
      // https://plaid.com/docs/api/tokens/#token-exchange-flow
      if (userRef.current) {
        setAccessToken(publicToken, userRef.current?.uid);
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