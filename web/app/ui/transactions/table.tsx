import { Transaction } from '@/app/lib/model';
import * as server from  '@/app/services/bettermint';
import { DeleteTransaction, EditTransaction } from '@/app/ui/transactions/buttons';
import Pagination from '@/app/ui/transactions/pagination';

export default async function TransactionsTable({
    userId,
    query,
    currentPage
}: {
    userId: string;
    query: string;
    currentPage: number;
}) {

    var response = await server.getTransactions(userId, query, currentPage);
    const totalPages = response.pagination?.total_pages || 1;

    return (<>
        <div className="mt-6 flow-root">
            <div className="inline-block min-w-full align-middle">
                <div className="rounded-lg bg-gray-50 p-2 md:pt-0">
                    <div className="md:hidden">
                        {/* TODO: this section is for small screens and has not been maintained */}
                        {response.data?.map((transaction: Transaction) => (
                            <div
                                key={transaction.id}
                                className="mb-2 w-full rounded-md bg-white p-4"
                            >
                                <div className="flex items-center justify-between border-b pb-4">
                                    <div>
                                        <div className="mb-2 flex items-center">
                                            <p>{transaction.name}</p>
                                        </div>
                                    </div>
                                </div>
                                <div className="flex w-full items-center justify-between pt-4">
                                    <div>
                                        <p className="text-xl font-medium">
                                            {transaction.amount.toLocaleString('en-CA', {
                                                style: 'currency',
                                                currency: 'CAD'
                                            })}
                                        </p>
                                        <p>
                                            {new Date(transaction.date).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <table className="hidden min-w-full text-gray-900 md:table">
                        <thead className="rounded-lg text-left text-sm font-normal">
                            <tr>
                                <th scope="col" className="px-3 py-5 font-medium">
                                    Date
                                </th>
                                <th scope="col" className="px-4 py-5 font-medium sm:pl-6">
                                    Description
                                </th>
                                <th scope="col" className="px-4 py-5 font-medium sm:pl-6">
                                    Category
                                </th>
                                <th scope="col" className="px-3 py-5 font-medium">
                                    Amount
                                </th>
                                <th scope="col" className="px-3 py-5 font-medium">
                                    Note
                                </th>
                            </tr>
                        </thead>
                        <tbody className="bg-white">
                            {response.data?.map((transaction: Transaction) => (
                                <tr
                                    key={transaction.id}
                                    className="w-full border-b py-3 text-sm last-of-type:border-none [&:first-child>td:first-child]:rounded-tl-lg [&:first-child>td:last-child]:rounded-tr-lg [&:last-child>td:first-child]:rounded-bl-lg [&:last-child>td:last-child]:rounded-br-lg"
                                >
                                    <td className="whitespace-nowrap px-3 py-3">
                                        {new Date(transaction.date).toLocaleDateString()}
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-3">
                                        {transaction.name}
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-3">
                                        {transaction.category_name}
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-3">
                                        {transaction.amount.toLocaleString('en-CA', {
                                            style: 'currency',
                                            currency: 'CAD'
                                        })}
                                    </td>
                                    <td className="whitespace-nowrap px-3 py-3">
                                        {transaction.note}
                                    </td>
                                    <td className="whitespace-nowrap py-3 pl-6 pr-3">
                                        <div className="flex justify-end gap-3">
                                            <EditTransaction id={transaction.id} />
                                            <DeleteTransaction id={transaction.id} />
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div className="mt-5 flex w-full justify-center">
            <Pagination totalPages={totalPages} />
        </div>
    </>)
}
