import Breadcrumbs from '@/app/ui/invoices/breadcrumbs';
import Form from '@/app/ui/invoices/create-form';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Create Transaction',
};

export default async function Page() {
    return (
        <main>
            <Breadcrumbs breadcrumbs={[
                {
                    label: 'Transactions',
                    href: '/dashboard/transactions'
                }, {
                    label: 'Create Transaction',
                    href: '/dashboard/transactions/create',
                    active: true
                }
            ]} />
            <Form />
        </main>
    );
}