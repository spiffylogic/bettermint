import { Account } from '@/app/lib/model';
import * as server from  '@/app/services/bettermint';
import getServerUser from "@/app/lib/firebase/getServerUser";

export default async function Accounts() {
    const user = await getServerUser();
    const accounts = await server.getAccounts(user?.uid ?? "");

    return (
        <div>
            <h1>Accounts Page</h1>
            <p>USERID: {user?.uid}</p>
            <center>
                { accounts.map((account: Account, index: number) => {
                    return (
                        <div key={index}>
                            <p>{ account.number  + " " + account.name }</p>
                        </div>
                    );
                })}
            </center>
        </div>
    );
}