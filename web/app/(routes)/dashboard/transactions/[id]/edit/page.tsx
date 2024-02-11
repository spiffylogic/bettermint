import EditTransactionForm from '@/app/ui/transactions/edit-form';
import Breadcrumbs from '@/app/ui/transactions/breadcrumbs';
import * as server from  '@/app/services/bettermint';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Edit Transaction',
};

export default async function Page({ params }: { params: { id: string } }) {
  const id = params.id;
  const transaction = await server.getTransaction(id);

  if (!transaction) {
    notFound();
  }

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: 'Transactions', href: '/dashboard/transactions' },
          {
            label: 'Edit Transaction',
            href: `/dashboard/transactions/${id}/edit`,
            active: true,
          },
        ]}
      />
      <EditTransactionForm transaction={transaction} />
    </main>
  );
}
