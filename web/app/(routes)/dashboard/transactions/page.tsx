import getServerUser from '@/app/lib/firebase/getServerUser';
import { lusitana } from "@/app/ui/fonts";
import Search from '@/app/ui/search';
import { ClientRefresh, ServerRefresh, CreateTransaction } from '@/app/ui/transactions/buttons';
import TransactionsTable from "@/app/ui/transactions/table";

export default async function Page({
    searchParams,
}: {
    searchParams?: {
        query?: string;
        page?: string;
    };
}) {

    const user = await getServerUser();
    const userId = user?.uid ?? "";

    const query = searchParams?.query || '';
    const currentPage = Number(searchParams?.page) || 1;

    return (
        <div className="w-full">
        <div className="flex w-full items-center justify-between">
          <h1 className={`${lusitana.className} text-2xl`}>Transactions</h1>
        </div>
        <div  className="mt-4 flex items-center justify-normal gap-2 md:mt-8">
            <ClientRefresh />
            <ServerRefresh userId={userId} />
        </div>
        <div  className="mt-4 flex items-center justify-normal gap-2 md:mt-8">
            <Search placeholder="Search transactions..." />
            <CreateTransaction />
        </div>
        <TransactionsTable userId={userId} query={query} currentPage={currentPage} />
      </div>
    );
}
