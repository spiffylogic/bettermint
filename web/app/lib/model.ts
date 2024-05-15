export interface Account {
    number: string;
    name: string;
}

export interface Transaction {
    id: string;
    category_id: string;
    category_name: string;
    date: Date;
    name: string;
    amount: number;
    note: string;
    tags: string[];
}

export interface Category {
    id: string;
    name: string;
}
