'use client';

import { ArrowPathRoundedSquareIcon, ArrowsUpDownIcon, PencilIcon } from '@heroicons/react/24/outline';
import * as server from  '@/app/services/bettermint';

import Link from 'next/link';
import { useRouter } from 'next/navigation';

export function ClientRefresh() {
    const router = useRouter();

    return (
        <button
            className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            onClick={() => { router.refresh(); }}
        >
            <span className="hidden md:block">Refresh</span>{' '}
            <ArrowsUpDownIcon className="h-5 md:ml-4" />
        </button>
    );

}

export function ServerRefresh({ userId }: { userId: string }) {
    const router = useRouter();

    async function sync(id: string) {
        console.log("SERVER SYNC")
        const data = await server.syncTransactions(id);
        console.log(data);
        // Check if there is new data to refresh
        if (data && data.length == 3 && (data[0] > 0 || data[1] > 0 || data[2] > 0)) {
            router.refresh()
        }
    }
    const syncWithUserId = sync.bind(null, userId);

    return (
        <button
            className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            onClick={syncWithUserId}
        >
            <span className="hidden md:block">Sync</span>{' '}
            <ArrowPathRoundedSquareIcon className="h-5 md:ml-4" />
        </button>
    );
}

export function EditTransaction({ id }: { id: string }) {
    return (
      <Link
        href={`/dashboard/transactions/${id}/edit`}
        className="rounded-md border p-2 hover:bg-gray-100"
      >
        <PencilIcon className="w-5" />
      </Link>
    );
  }
  
/*  export function DeleteTransaction({ id }: { id: string }) {
    const deleteInvoiceWithId = deleteTransaction.bind(null, id);
  
    return (
      <form action={deleteInvoiceWithId}>
        <button className="rounded-md border p-2 hover:bg-gray-100">
          <span className="sr-only">Delete</span>
          <TrashIcon className="w-5" />
        </button>
      </form>
    );
  }
*/