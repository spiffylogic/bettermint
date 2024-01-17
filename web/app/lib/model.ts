export interface Account {
    number: string;
    name: string;
}

export interface Transaction {
    id: string;
    category: string;
    date: Date;
    name: string;
    amount: number;
}