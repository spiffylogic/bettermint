import getServerUser from '@/app/lib/firebase/getServerUser';
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

    const user = await getServerUser();
    const userId = user?.uid ?? "";

	const transaction = await server.getTransaction(id);
	const categories = await server.getCategories(userId);

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
			<EditTransactionForm
				transaction={transaction}
				categories={categories}
			/>
		</main>
	);
}
