'use client';

import { Transaction } from '@/app/lib/model';
import { modifyTransaction } from '@/app/services/bettermint';
import { Button } from '@/app/ui/button';

import { CurrencyDollarIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

async function updateTransaction(id: string, formData: FormData) {
    const tx: Transaction = {
        id: id,
        category: '',
        date: new Date(), // TODO: get date from string form data
        name: formData.get('name')?.toString() || '',
        amount: Number(formData.get('amount')),
        note: formData.get('note')?.toString() || '',
    };
    modifyTransaction(tx);
}

export default function EditTransactionForm({transaction}: {transaction: Transaction}) {
  // We want to pass the id to the Server Action so you can update the right record.
  // You cannot simply pass the id as an argument. Instead, you can pass id to the Server Action
  // using JS bind. This will ensure that any values passed to the Server Action are encoded.
  const updateTransactionWithId = updateTransaction.bind(null, transaction.id);

  return (
    <form action={updateTransactionWithId}>
      <div className="rounded-md bg-gray-50 p-4 md:p-6">

        {/* Transaction Amount */}
        <div className="mb-4">
          <label htmlFor="amount" className="mb-2 block text-sm font-medium">
            Choose an amount
          </label>
          <div className="relative mt-2 rounded-md">
            <div className="relative">
              <input
                id="amount"
                name="amount"
                type="number"
                step="0.01"
                defaultValue={transaction.amount}
                placeholder="Enter CAD amount"
                className="peer block w-full rounded-md border border-gray-200 py-2 pl-10 text-sm outline-2 placeholder:text-gray-500"
                aria-describedby='amount-error'
              />
              <CurrencyDollarIcon className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" />
            </div>
            <div id="amount-error" aria-live="polite" aria-atomic="true">
              {/* {state.errors?.amount &&
                state.errors.amount.map((error: string) => (
                  <p className="mt-2 text-sm text-red-500" key={error}>
                    {error}
                  </p>
                ))} */}
            </div>
          </div>
        </div>
      </div>
      <div className="mt-6 flex justify-end gap-4">
        <Link
          href="/dashboard/transactions"
          className="flex h-10 items-center rounded-lg bg-gray-100 px-4 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-200"
        >
          Cancel
        </Link>
        <Button type="submit">Edit Transaction</Button>
      </div>
    </form>
  );
}
