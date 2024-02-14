// import { fetchCustomers } from '@/app/lib/data';
import Breadcrumbs from '@/app/ui/transactions/breadcrumbs';
// import Form from '@/app/ui/invoices/create-form';
import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Create Transaction',
};

export default async function Page() {
    // const customers = await fetchCustomers();

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
            {/* <Form customers={customers} /> */}
        </main>
    );
}