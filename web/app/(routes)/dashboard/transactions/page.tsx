import getServerUser from '@/app/lib/firebase/getServerUser';
import * as server from  '@/app/services/bettermint';
import { lusitana } from "@/app/ui/fonts";
import { ClientRefresh, ServerRefresh } from '@/app/ui/transactions-buttons';
import TransactionsTable from "@/app/ui/transactions-table";

export default async function Transactions() {
    const user = await getServerUser();
    const userId = user?.uid ?? "";
    var transactions = await server.getTransactions(userId);
    console.log(`LOADED ${transactions.length} TRANSACTIONS FOR ${userId}`);

    return (
        <div className="w-full">
        <div className="flex w-full items-center justify-between">
          <h1 className={`${lusitana.className} text-2xl`}>Transactions</h1>
        </div>
        <div  className="mt-4 flex items-center justify-normal gap-2 md:mt-8">
            <ClientRefresh />
            <ServerRefresh userId={userId} />
        </div>
        <TransactionsTable transactions={transactions} />
      </div>
    );
}
