import getServerUser from '@/app/lib/firebase/getServerUser';
import Breadcrumbs from '@/app/ui/transactions/breadcrumbs';
import CreateTransactionForm from '@/app/ui/transactions/create-form';

import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Create Transaction',
};

export default async function Page() {
    const user = await getServerUser();
    const userId = user?.uid ?? "";

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
            <CreateTransactionForm userId={userId} />
        </main>
    );
}