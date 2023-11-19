export interface Account {
    number: string;
    name: string;
}

export interface Transaction {
    category: string;
    date: Date;
    name: string;
    amount: number;
}