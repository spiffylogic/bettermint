'use server';

import { Transaction } from "@/app/lib/model";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { PlaidAccount } from 'react-plaid-link';

const transactionsPath = '/dashboard/transactions';

export const createLinkToken = async () => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/create_link_token`, { method: 'POST' });
    const { link_token } = await response.json();
    return link_token
};

export const setAccessToken = async (publicToken: string, userId: string | null) => {
    console.log(`Sending public token ${publicToken} for user ${userId}`);
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: userId,
            public_token: publicToken
        })
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/set_access_token`, requestOptions);
};

export const saveAccounts = async (accounts: Array<PlaidAccount>, userId: string) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            accounts: accounts.map((value: PlaidAccount, index: number, array: PlaidAccount[]) => {
                return {
                    id: value.id,
                    name: value.name,
                    number: value.mask
                }
            })
        })
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/accounts?user_id=${userId}`, requestOptions);
}

export async function getAccounts(userId: string) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/accounts?user_id=${userId}`, { method: 'GET' });
    const data = await response.json();
    return data;
};

export const getTransactions = async (userId: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions?user_id=${userId}`, { method: 'GET' });
    const data = await response.json();
    return data;
};

export async function getTransaction(id: string) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/${id}`, { method: 'GET' });
    const data = await response.json();
    return data;
}

export async function modifyTransaction(transaction: Transaction) {
    console.log(transaction);
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction)
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/${transaction.id}`, requestOptions);
    revalidatePath(transactionsPath);
    redirect(transactionsPath);
}

export const syncTransactions = async (userId: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/sync?user_id=${userId}`, { method: 'POST' });
    const data = await response.json();
    return data;
};
