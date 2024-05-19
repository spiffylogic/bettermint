'use client'

import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import {
    usePlaidLink,
    // PlaidLinkOptions,
    PlaidLinkOnSuccess,
  } from 'react-plaid-link';
import * as server from  '@/app/services/bettermint';
import useUser from '@/app/lib/firebase/getUser';

export default function Link() {
    const [token, setToken] = useState<string | null>(null);
    const user = useUser();

    // These seems to be necessary otherwise we lose the user
    // when the component is recreated after returning from the Link UI
    const userRef = useRef(user);
    userRef.current = user;

    // get link_token from your server when component mounts
    useEffect(() => {
        // self-invoking async function, since useEffect is not async
        (async() => {
            const link_token = await server.createLinkToken();
            setToken(link_token);
        })()
    }, []);

    const onSuccess = useCallback<PlaidLinkOnSuccess>((publicToken, metadata) => {
      // https://plaid.com/docs/api/tokens/#token-exchange-flow
      if (userRef.current) {
        const userId = userRef.current?.uid;
        server.setAccessToken(publicToken, userId);
        server.saveAccounts(metadata.accounts, userId);
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