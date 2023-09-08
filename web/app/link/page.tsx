'use client'

import { useCallback, useEffect, useState } from 'react';
import {
    usePlaidLink,
    PlaidLinkOptions,
    PlaidLinkOnSuccess,
  } from 'react-plaid-link';

export default function Link() {
    const [token, setToken] = useState<string | null>(null);

    // get link_token from your server when component mounts
    useEffect(() => {
      const createLinkToken = async () => {
        console.log(`MARKUS requesting link token`);
        const response = await fetch('http://localhost:5000/create_link_token', { method: 'POST' });
        const { link_token } = await response.json();
        setToken(link_token);
        console.log(`MARKUS created token ${link_token}`);
      };
      createLinkToken();
    }, []);

    const onSuccess = useCallback<PlaidLinkOnSuccess>((publicToken, metadata) => {
      // send public_token to your server
      // https://plaid.com/docs/api/tokens/#token-exchange-flow
      console.log(publicToken, metadata);
    }, []);

    const { open, ready } = usePlaidLink({
      token,
      onSuccess,
      // onEvent
      // onExit
    });

    return (
      <button onClick={() => open()} disabled={!ready}>
        Connect a bank account
      </button>
    );
}