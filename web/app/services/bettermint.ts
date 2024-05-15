'use server';

import { Transaction } from "@/app/lib/model";

import { revalidatePath, unstable_noStore as noStore } from "next/cache";
import { redirect } from "next/navigation";
import { PlaidAccount } from 'react-plaid-link';

const transactionsPath = '/dashboard/transactions';

export const createLinkToken = async () => {
    noStore();
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
    noStore();
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/accounts?user_id=${userId}`, { method: 'GET' });
    const data = await response.json();
    return data;
};

export async function getTransactions(userId: string, query: string, currentPage: number) {
    noStore();
    var url = `${process.env.NEXT_PUBLIC_SERVER_URL}/transactions?user_id=${userId}&page=${currentPage}`;
    if (query) {
        url += `&q=${query}`;
    }
    const response = await fetch(url, { method: 'GET' });
    const data = await response.json();
    return data;
}

export async function getTransaction(id: string) {
    noStore();
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/${id}`, { method: 'GET' });
    const data = await response.json();
    return data;
}

export async function createTransaction(userId: string, transaction: Transaction) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction)
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions?user_id=${userId}`, requestOptions);
    revalidatePath(transactionsPath);
    redirect(transactionsPath);
}

export async function modifyTransaction(transaction: Transaction) {
    const requestOptions = {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction)
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/${transaction.id}`, requestOptions);
    revalidatePath(transactionsPath);
    redirect(transactionsPath);
}

export async function removeTransaction(id: string) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/${id}`, { method: 'DELETE' });
    const data = await response.json();
    return data;
}

export const syncTransactions = async (userId: string) => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/transactions/sync?user_id=${userId}`, { method: 'POST' });
    const data = await response.json();
    return data;
};

export async function getCategories(userId: string) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_SERVER_URL}/categories?user_id=${userId}`, { method: 'GET' });
    const data = await response.json();
    return data;
}

export async function createCategory(userId: string, name: string) {
    console.log(`CREATE CATEGORY ${name}`);
}

export async function modifyCategory(userId: string, categoryId: string, name: string) {
    console.log(`MODIFY CATEGORY ${categoryId} -> ${name}`);
}
